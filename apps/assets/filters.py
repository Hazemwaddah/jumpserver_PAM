# -*- coding: utf-8 -*-
#
from django.db.models import Q
from django_filters import rest_framework as drf_filters
from rest_framework import filters
from rest_framework.compat import coreapi, coreschema

from assets.utils import get_node_from_request, is_query_node_all_assets
from common.drf.filters import BaseFilterSet

from .models import Account, Label, Node


class AssetByNodeFilterBackend(filters.BaseFilterBackend):
    fields = ['node', 'all']

    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name=field, location='query', required=False,
                type='string', example='', description='', schema=None,
            )
            for field in self.fields
        ]

    def filter_node_related_all(self, queryset, node):
        return queryset.filter(
            Q(nodes__key__istartswith=f'{node.key}:') |
            Q(nodes__key=node.key)
        ).distinct()

    def filter_node_related_direct(self, queryset, node):
        return queryset.filter(nodes__key=node.key).distinct()

    def filter_queryset(self, request, queryset, view):
        node = get_node_from_request(request)
        if node is None:
            return queryset

        query_all = is_query_node_all_assets(request)
        if query_all:
            return self.filter_node_related_all(queryset, node)
        else:
            return self.filter_node_related_direct(queryset, node)


class NodeFilterBackend(filters.BaseFilterBackend):
    """
    需要与 `assets.api.mixin.NodeFilterMixin` 配合使用
    """
    fields = ['node', 'all']

    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name=field, location='query', required=False,
                type='string', example='', description='', schema=None,
            )
            for field in self.fields
        ]

    def filter_queryset(self, request, queryset, view):
        node = get_node_from_request(request)
        if node is None:
            return queryset

        query_all = is_query_node_all_assets(request)
        if query_all:
            return queryset.filter(
                Q(nodes__key__istartswith=f'{node.key}:') |
                Q(nodes__key=node.key)
            ).distinct()
        else:
            print("Query query origin: ", queryset.count())
            return queryset.filter(nodes__key=node.key).distinct()


class LabelFilterBackend(filters.BaseFilterBackend):
    sep = ':'
    query_arg = 'label'

    def get_schema_fields(self, view):
        example = self.sep.join(['os', 'linux'])
        return [
            coreapi.Field(
                name=self.query_arg, location='query', required=False,
                type='string', example=example, description=''
            )
        ]

    def get_query_labels(self, request):
        labels_query = request.query_params.getlist(self.query_arg)
        if not labels_query:
            return None

        q = None
        for kv in labels_query:
            if '#' in kv:
                self.sep = '#'
                break

        for kv in labels_query:
            if self.sep not in kv:
                continue
            key, value = kv.strip().split(self.sep)[:2]
            if not all([key, value]):
                continue
            if q:
                q |= Q(name=key, value=value)
            else:
                q = Q(name=key, value=value)
        if not q:
            return []
        labels = Label.objects.filter(q, is_active=True) \
            .values_list('id', flat=True)
        return labels

    def filter_queryset(self, request, queryset, view):
        labels = self.get_query_labels(request)
        if labels is None:
            return queryset
        if len(labels) == 0:
            return queryset.none()
        for label in labels:
            queryset = queryset.filter(labels=label)
        return queryset


class AssetRelatedByNodeFilterBackend(AssetByNodeFilterBackend):
    def filter_node_related_all(self, queryset, node):
        return queryset.filter(
            Q(asset__nodes__key__istartswith=f'{node.key}:') |
            Q(asset__nodes__key=node.key)
        ).distinct()

    def filter_node_related_direct(self, queryset, node):
        return queryset.filter(asset__nodes__key=node.key).distinct()


class IpInFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        ips = request.query_params.get('ips')
        if not ips:
            return queryset
        ip_list = [i.strip() for i in ips.split(',')]
        queryset = queryset.filter(address__in=ip_list)
        return queryset

    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name='ips', location='query', required=False, type='string',
                schema=coreschema.String(
                    title='ips',
                    description='address in filter'
                )
            )
        ]


class AccountFilterSet(BaseFilterSet):
    ip = drf_filters.CharFilter(field_name='address', lookup_expr='exact')
    hostname = drf_filters.CharFilter(field_name='name', lookup_expr='exact')
    username = drf_filters.CharFilter(field_name="username", lookup_expr='exact')
    address = drf_filters.CharFilter(field_name="asset__address", lookup_expr='exact')
    asset = drf_filters.CharFilter(field_name="asset_id", lookup_expr='exact')
    assets = drf_filters.CharFilter(field_name='asset_id', lookup_expr='exact')
    nodes = drf_filters.CharFilter(method='filter_nodes')
    has_secret = drf_filters.BooleanFilter(method='filter_has_secret')

    @staticmethod
    def filter_has_secret(queryset, name, has_secret):
        q = Q(secret__isnull=True) | Q(secret='')
        if has_secret:
            return queryset.exclude(q)
        else:
            return queryset.filter(q)

    @staticmethod
    def filter_nodes(queryset, name, value):
        nodes = Node.objects.filter(id=value)
        if not nodes:
            return queryset

        node_qs = Node.objects.none()
        for node in nodes:
            node_qs |= node.get_all_children(with_self=True)
        node_ids = list(node_qs.values_list('id', flat=True))
        queryset = queryset.filter(asset__nodes__in=node_ids)
        return queryset

    class Meta:
        model = Account
        fields = ['id']

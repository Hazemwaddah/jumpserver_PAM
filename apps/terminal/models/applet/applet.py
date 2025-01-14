import yaml
import os.path

from django.conf import settings
from django.core.files.storage import default_storage
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.db.models import JMSBaseModel


__all__ = ['Applet', 'AppletPublication']


class Applet(JMSBaseModel):
    class Type(models.TextChoices):
        general = 'general', _('General')
        web = 'web', _('Web')

    name = models.SlugField(max_length=128, verbose_name=_('Name'), unique=True)
    display_name = models.CharField(max_length=128, verbose_name=_('Display name'))
    version = models.CharField(max_length=16, verbose_name=_('Version'))
    author = models.CharField(max_length=128, verbose_name=_('Author'))
    type = models.CharField(max_length=16, verbose_name=_('Type'), default='general', choices=Type.choices)
    is_active = models.BooleanField(default=True, verbose_name=_('Is active'))
    protocols = models.JSONField(default=list, verbose_name=_('Protocol'))
    tags = models.JSONField(default=list, verbose_name=_('Tags'))
    comment = models.TextField(default='', blank=True, verbose_name=_('Comment'))
    hosts = models.ManyToManyField(
        through_fields=('applet', 'host'), through='AppletPublication',
        to='AppletHost', verbose_name=_('Hosts')
    )

    def __str__(self):
        return self.name

    @property
    def path(self):
        return default_storage.path('applets/{}'.format(self.name))

    @property
    def manifest(self):
        path = os.path.join(self.path, 'manifest.yml')
        if not os.path.exists(path):
            return None
        with open(path, 'r') as f:
            return yaml.safe_load(f)

    @property
    def icon(self):
        path = os.path.join(self.path, 'icon.png')
        if not os.path.exists(path):
            return None
        return os.path.join(settings.MEDIA_URL, 'applets', self.name, 'icon.png')


class AppletPublication(JMSBaseModel):
    applet = models.ForeignKey('Applet', on_delete=models.PROTECT, related_name='publications', verbose_name=_('Applet'))
    host = models.ForeignKey('AppletHost', on_delete=models.PROTECT, related_name='publications', verbose_name=_('Host'))
    status = models.CharField(max_length=16, default='ready', verbose_name=_('Status'))
    comment = models.TextField(default='', blank=True, verbose_name=_('Comment'))

    class Meta:
        unique_together = ('applet', 'host')

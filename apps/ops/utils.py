# ~*~ coding: utf-8 ~*~
import os
import uuid

from django.utils.translation import ugettext_lazy as _

from common.utils import get_logger, get_object_or_none
from orgs.utils import org_aware_func
from jumpserver.const import PROJECT_DIR

from .models import AdHoc, CeleryTask
from .const import DEFAULT_PASSWORD_RULES

logger = get_logger(__file__)

DEFAULT_TASK_OPTIONS = {
    'timeout': 10,
    'forks': 10,
}


def get_task_by_id(task_id):
    return get_object_or_none(Task, id=task_id)


@org_aware_func("hosts")
def update_or_create_ansible_task(
        task_name, hosts, tasks,
        interval=None, crontab=None, is_periodic=False,
        callback=None, pattern='all', options=None,
        run_as_admin=False, run_as=None, system_user=None, become_info=None,
):
    if not hosts or not tasks or not task_name:
        return None, None
    if options is None:
        options = DEFAULT_TASK_OPTIONS
    defaults = {
        'name': task_name,
        'interval': interval,
        'crontab': crontab,
        'is_periodic': is_periodic,
        'callback': callback,
    }

    created = False
    task, ok = Task.objects.update_or_create(
        defaults=defaults, name=task_name
    )
    adhoc = task.get_latest_adhoc()
    new_adhoc = AdHoc(task=task, pattern=pattern,
                      run_as_admin=run_as_admin,
                      run_as=run_as, run_system_user=system_user)
    new_adhoc.tasks = tasks
    new_adhoc.options = options
    new_adhoc.become = become_info

    hosts_same = True
    if adhoc:
        old_hosts = set([str(asset.id) for asset in adhoc.hosts.all()])
        new_hosts = set([str(asset.id) for asset in hosts])
        hosts_same = old_hosts == new_hosts

    if not adhoc or not adhoc.same_with(new_adhoc) or not hosts_same:
        logger.debug(_("Update task content: {}").format(task_name))
        new_adhoc.save()
        new_adhoc.hosts.set(hosts)
        task.latest_adhoc = new_adhoc
        created = True
    return task, created


def get_task_log_path(base_path, task_id, level=2):
    task_id = str(task_id)
    try:
        uuid.UUID(task_id)
    except:
        return os.path.join(PROJECT_DIR, 'data', 'caution.txt')

    rel_path = os.path.join(*task_id[:level], task_id + '.log')
    path = os.path.join(base_path, rel_path)
    make_dirs(os.path.dirname(path), exist_ok=True)
    return path


def generate_random_password(**kwargs):
    import random
    import string
    length = int(kwargs.get('length', DEFAULT_PASSWORD_RULES['length']))
    symbol_set = kwargs.get('symbol_set')
    if symbol_set is None:
        symbol_set = DEFAULT_PASSWORD_RULES['symbol_set']
    chars = string.ascii_letters + string.digits + symbol_set
    password = ''.join([random.choice(chars) for _ in range(length)])
    return password

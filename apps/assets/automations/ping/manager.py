from common.utils import get_logger
from assets.const import AutomationTypes, Connectivity
from ..base.manager import BasePlaybookManager

logger = get_logger(__name__)


class PingManager(BasePlaybookManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.host_asset_and_account_mapper = {}

    @classmethod
    def method_type(cls):
        return AutomationTypes.ping

    def host_callback(self, host, asset=None, account=None, **kwargs):
        super().host_callback(host, asset=asset, account=account, **kwargs)
        self.host_asset_and_account_mapper[host['name']] = (asset, account)
        return host

    def on_host_success(self, host, result):
        asset, account = self.host_asset_and_account_mapper.get(host)
        asset.set_connectivity(Connectivity.OK)
        if not account:
            return
        account.set_connectivity(Connectivity.OK)

    def on_host_error(self, host, error, result):
        asset, account = self.host_asset_and_account_mapper.get(host)
        asset.set_connectivity(Connectivity.FAILED)
        if not account:
            return
        account.set_connectivity(Connectivity.FAILED)

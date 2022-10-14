from django.utils.translation import ugettext_lazy as _

from ops.const import StrategyChoice
from .base import BaseAutomation


class VerifyAutomation(BaseAutomation):
    class Meta:
        verbose_name = _("Verify strategy")

    def save(self, *args, **kwargs):
        self.type = 'verify'
        super().save(*args, **kwargs)

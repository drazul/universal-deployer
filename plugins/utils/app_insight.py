import logging

from .process import execute

__name__ = 'universal_deployer'
logger = logging.getLogger(__name__)


def activate(name, key):
    cmd = 'powershell Import-Module \
        "C:/Program Files/Microsoft Application Insights/Status Monitor/PowerShell/Microsoft.Diagnostics.Agent.StatusMonitor.PowerShell.dll"; \
        Start-ApplicationInsightsMonitoring -Name {name} -InstrumentationKey {key}'.format(
        name=name, key=key)
    execute(cmd)

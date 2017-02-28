import logging
import sys
import time

from .process import execute

__name__ = 'universal_deployer'
logger = logging.getLogger(__name__)


def create(service_name, executable_path, arguments=None):
    cmd = 'nssm install {service_name} {executable_path} {arguments}'.format(
        service_name=service_name, executable_path=executable_path,
        arguments=arguments)
    execute(cmd)


def remove(service_name):
    cmd = 'nssm remove {service_name} confirm'.format(
            service_name=service_name)
    execute(cmd)


def start(service_name):
    return_code = 1
    tries = 0
    while return_code is not 0 and tries < 42:
        time.sleep(tries)
        tries *= (tries + 1)

        cmd = 'nssm start {service_name}'.format(service_name=service_name)
        return_code = execute(cmd, ignore_errors=True)

    if return_code is not 0:
        logger.error(
            '{service_name} failed to start!'.format(
                service_name=service_name))
        sys.exit(return_code)
    else:
        logger.info('{service_name} started!'.format(
                service_name=service_name))


def stop(service_name):
    cmd = 'nssm stop {service_name}'.format(service_name=service_name)
    execute(cmd)


def set_delay_after_restart(service_name, delay):
    cmd = 'nssm set {service_name} AppThrottle {delay}'.format(
        service_name=service_name, delay=delay)
    execute(cmd)


def status(service_name):
    cmd = 'nssm status {service_name}'.format(service_name=service_name)
    execute(cmd, ignore_errors=True)

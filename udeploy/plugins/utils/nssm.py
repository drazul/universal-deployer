import sys
import time

from .process import execute

from logger import logger


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
    while return_code is not 0 and tries < 6:
        time_to_sleep = tries * tries
        logger.info('Starting {service_name} in {time} seconds'.format(
            service_name=service_name, time=time_to_sleep
        ))
        time.sleep(time_to_sleep)

        cmd = 'nssm start {service_name}'.format(service_name=service_name)
        return_code = execute(cmd, ignore_errors=True)
        tries += 1

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

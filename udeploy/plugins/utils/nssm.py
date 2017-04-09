import sys
import time

from .process import execute

from logger import logger


def create(service_name, executable_path, arguments=None):
    cmd = 'nssm install {service_name} {executable_path} {arguments}'.format(
        service_name=service_name, executable_path=executable_path,
        arguments=arguments if arguments else '')
    execute(cmd, ignore_errors=True)


def remove(service_name):
    cmd = 'nssm remove {service_name} confirm'.format(
            service_name=service_name)
    execute(cmd, ignore_errors=True)


def start(service_name):
    tries = 0
    running = False
    response = dict()

    while not running and tries < 6:
        time_to_sleep = tries * tries
        logger.info('Starting {service_name} in {time} seconds'.format(
            service_name=service_name, time=time_to_sleep
        ))
        time.sleep(time_to_sleep)

        cmd = 'nssm start {service_name}'.format(service_name=service_name)
        response = execute(cmd, ignore_errors=True)
        tries += 1
        running = (
            status(service_name)['stdout'][0].strip() == 'SERVICE_RUNNING')

    if not running and response['return_code'] is not 0:
        logger.error(
            '{service_name} failed to start!'.format(
                service_name=service_name))
        sys.exit(response['return_code'])
    else:
        logger.info('{service_name} started!'.format(
                service_name=service_name))


def stop(service_name):
    cmd = 'nssm stop {service_name}'.format(service_name=service_name)
    execute(cmd, ignore_errors=True)


def status(service_name):
    cmd = 'nssm status {service_name}'.format(service_name=service_name)
    return execute(cmd, ignore_errors=True)


def set_delay_after_restart(service_name, delay):
    cmd = 'nssm set {service_name} AppThrottle {delay}'.format(
        service_name=service_name, delay=delay)
    execute(cmd)


def set_stdout_log_file(service_name, path):
    cmd = 'nssm set {service_name} AppStdout {path}'.format(
        service_name=service_name, path=path)
    execute(cmd)


def set_stderr_log_file(service_name, path):
    cmd = 'nssm set {service_name} AppStderr {path}'.format(
        service_name=service_name, path=path)
    execute(cmd)


def set_log_rotation(service_name, rotation_in_bytes=None,
                     rotation_in_seconds=None):
    cmd = 'nssm set {service_name} AppRotateFiles 1'.format(
        service_name=service_name)
    execute(cmd)

    if rotation_in_bytes:
        cmd = 'nssm set {service_name} AppRotateBytes {value}'.format(
            service_name=service_name, value=rotation_in_bytes)
        execute(cmd)

    if rotation_in_seconds:
        cmd = 'nssm set {service_name} AppRotateSeconds {value}'.format(
            service_name=service_name, value=rotation_in_seconds)
        execute(cmd)


def set_custom_environment_variables(service_name, environment_list):
    environment_str = ' '.join(environment_list)
    cmd = 'nssm set {service_name} AppEnvironmentExtra {environment}'.format(
        service_name=service_name, environment=environment_str)
    execute(cmd)

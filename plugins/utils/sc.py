from .process import execute

def create(service_name, exec_path):
    cmd = 'sc.exe create {service_name} start=auto binpath={exec_path}'.format(
        service_name=service_name, exec_path=exec_path)
    execute(cmd)


def remove(service_name):
    cmd = 'sc.exe delete {service_name}'.format(service_name=service_name)
    execute(cmd)


def start(service_name):
    cmd = 'sc.exe start {service_name}'.format(service_name=service_name)
    execute(cmd)


def stop(service_name):
    cmd = 'sc.exe stop {service_name}'.format(service_name=service_name)
    execute(cmd)


def kill(exec_file):
    cmd = 'taskkill /im {exec_file} /F'.format(exec_file=exec_file)
    execute(cmd)

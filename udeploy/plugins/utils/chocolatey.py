from .process import execute

from logger import logger

download_path = 'C:/ProgramData/chocolatey/lib'


def install(package_name, version, source=None, download_only=False):
    if _is_installed(package_name, version):
        logger.info(
            '{package_name} {version} currently installed. Skipping'.format(
                package_name=package_name,
                version=version))
        return

    cmd = ('choco install {package_name} -version {version} '
           '-force --allow-downgrade').format(
        package_name=package_name, version=version)
    if source is not None:
        cmd += ' --source {source}'.format(source=source)
    if download_only:
        cmd += ' --skip-powershell'

    execute(cmd)


def get_installed_version(package_name):
    cmd = 'choco search --local-only {package_name}'.format(
        package_name=package_name)
    return execute(cmd)


def _is_installed(package_name, version):
    result = get_installed_version(package_name)
    if result['return_code'] == 0:
        installed_version = result['stdout'][0].split(' ')[1].strip()
        if installed_version == version:
            return True

    return False

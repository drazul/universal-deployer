import os

from .application_deployer import application_deployer
from .utils import chocolatey
from .utils import process
from logger import logger


class curator(application_deployer):

    def get_installed_version(self):
        super(curator, self).get_installed_version()
        chocolatey.get_installed_version(self.pkg_name)

    def download(self):
        super(curator, self).download()
        chocolatey.install(self.pkg_name, self.version,
                           source=self.global_config['choco_source'],
                           download_only=True)

    def deploy(self):
        super(curator, self).deploy()
        config_file = '{0}/{1}'.format(
            self.specific_config_path,
            'curator.yaml')
        if not os.path.isfile(config_file):
            config_file = '{0}/{1}'.format(
                self.generic_config_path,
                'curator.yaml')

        logger.debug('Using config file: {0}'.format(config_file))
        for f in self._find_files(self.install_path, '*.yaml'):
            logger.info('Executing file: {0}'.format(f))
            process.execute(
                'curator --config {config_file} {exec_file}'.format(
                        config_file=config_file,
                        exec_file=f))

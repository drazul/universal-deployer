import os

from .application_deployer import application_deployer
from .utils import chocolatey
from .utils import liquibase
from logger import logger


class databases(application_deployer):

    def __init__(
            self, name, app_config, app_type,
            weight, global_config, config_path, install_path):
        super(databases, self).__init__(name, app_config, app_type,
                weight, global_config, config_path, install_path)

        self.properties_file = ''

    def get_installed_version(self):
        super(databases, self).get_installed_version()
        chocolatey.get_installed_version(self.pkg_name)

    def download(self):
        super(databases, self).download()
        chocolatey.install(self.pkg_name, self.version,
                           source=self.global_config['choco_source'],
                           download_only=True)

    def configure(self):
        super(databases, self).configure()

        generic_config_file = self._find_files(
            self.generic_config_path, 'liquibase.properties')
        specific_config_file = self._find_files(
            self.specific_config_path, 'liquibase.properties')

        if len(specific_config_file) > 0:
            self.properties_file = specific_config_file[0]
        else:
            if len(generic_config_file) > 0:
                self.properties_file = generic_config_file[0]
            else:
                raise FileNotFoundError(
                    '{path}/liquibase.properties not found!'.format(
                        path=self.generic_config_path
                    ))

    def deploy_pre(self):
        super(databases, self).deploy_pre()

        if 'create_database' in self.params and \
                self.params['create_database']:
            liquibase.create_database(
                self.params['host'],
                self.params['db_name'],
                self.install_path + '/changelog-database.xml',
                self.properties_file)

        liquibase.update_database(
            self.params['host'],
            self.params['db_name'],
            self.install_path + '/changelog-latest-pre.xml',
            self.properties_file,
            self.params['arguments'],
            self.params['contexts'])

    def deploy_post(self):
        super(databases, self).deploy_post()

        liquibase.update_database(
            self.params['host'],
            self.params['db_name'],
            self.install_path + '/changelog-latest-post.xml',
            self.properties_file,
            self.params['arguments'],
            self.params['contexts'])
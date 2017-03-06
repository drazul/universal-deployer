from .application_deployer import application_deployer
from .utils import chocolatey
from .utils import liquibase


class databases(application_deployer):

    def _search_properties_file(self):
        generic_config_file = self._find_files(
            self.generic_config_path, 'liquibase.properties')
        specific_config_file = self._find_files(
            self.specific_config_path, 'liquibase.properties')

        if len(specific_config_file) > 0:
            return specific_config_file[0]
        else:
            if len(generic_config_file) > 0:
                return generic_config_file[0]
            else:
                raise FileNotFoundError(
                    '{path}/liquibase.properties not found!'.format(
                        path=self.generic_config_path
                    ))

    def get_installed_version(self):
        super(databases, self).get_installed_version()
        chocolatey.get_installed_version(self.pkg_name)

    def download(self):
        super(databases, self).download()
        chocolatey.install(self.pkg_name, self.version,
                           source=self.global_config['choco_source'],
                           download_only=True)

    def _execute_update(self, changelog_file_path, properties_file):
        liquibase.update_database(
            self.params['host'],
            self.params['database_name'],
            changelog_file_path,
            properties_file,
            self.params['arguments'] if 'arguments' in self.params else None,
            self.params['contexts'] if 'contexts' in self.params else None)

    def deploy_pre(self):
        super(databases, self).deploy_pre()
        properties_file = self._search_properties_file()

        if ('create_database' in self.params and
                self.params['create_database']):
            liquibase.create_database(
                self.params['host'],
                self.params['db_name'],
                self.install_path + '/changelog-database.xml',
                properties_file)
        self._execute_update(self.install_path + '/changelog-latest-pre.xml',
                             properties_file)

    def deploy_post(self):
        super(databases, self).deploy_post()
        properties_file = self._search_properties_file()

        self._execute_update(self.install_path + '/changelog-latest-post.xml',
                             properties_file)

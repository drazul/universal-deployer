import logging

from .application_deployer import application_deployer
from .utils import chocolatey
from .utils import iis_site

__name__ = 'universal_deployer'
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class iis_website(application_deployer):

    def get_installed_version(self):
        super(iis_website, self).get_installed_version()
        chocolatey.get_installed_version(self.pkg_name)

    def download(self):
        super(iis_website, self).download()
        chocolatey.install(self.pkg_name, self.version,
                           source=self.global_config['choco_source'],
                           download_only=True)

    def configure(self):
        super(iis_website, self).configure()
        self._copy_folder_templates(
            self.generic_config_path,
            '{0}/{1}'.format(self.install_path, 'Configs'),
            '*.config')
        self._copy_folder_templates(
            self.specific_config_path,
            '{0}/{1}'.format(self.install_path, 'Configs'),
            '*.config')

        if 'webconfig' in self.params:
            for key, value in self.params['webconfig'].items():
                iis_site.configure_webconfig(self.name, key, value)

        if 'replace' in self.params:
            files = self._find_files(
                self.install_path,
                self.params['replace']['file_pattern'])

            for filename in files:
                self._replacement_list_on_file(
                    filename,
                    self.params['replace']['patterns'])

    def deploy(self):
        super(iis_website, self).deploy()
        self.stop()

        self.download()
        self._sync_folders(
            '{0}/{1}'.format(chocolatey.download_path, self.pkg_name),
            self.install_path)
        self.configure()

        self.start()

    def start(self):
        super(iis_website, self).start()
        iis_site.start(self.name)

    def stop(self):
        super(iis_website, self).stop()
        iis_site.stop(self.name)

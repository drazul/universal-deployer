from .application_deployer import application_deployer
from .utils import chocolatey
from .utils import sc


class sc_service(application_deployer):

    def get_installed_version(self):
        super(sc_service, self).get_installed_version()
        chocolatey.get_installed_version(self.pkg_name)

    def download(self):
        super(sc_service, self).download()
        chocolatey.install(self.pkg_name, self.version,
                           source=self.global_config['choco_source']
                           if 'choco_source' in self.global_config
                           else None,
                           download_only=True)

    def configure(self):
        super(sc_service, self).configure()
        self._copy_folder_templates(
            self.generic_config_path,
            '{0}/{1}'.format(self.install_path, 'Configs'),
            '*.config')
        self._copy_folder_templates(
            self.specific_config_path,
            '{0}/{1}'.format(self.install_path, 'Configs'),
            '*.config')

    def deploy(self):
        super(sc_service, self).deploy()
        self.stop()
        self.remove()

        self.download()
        self._sync_folders(
            '{0}/{1}'.format(chocolatey.download_path, self.pkg_name),
            self.install_path)

        self.create()
        self.configure()

        self.start()

    def start(self):
        super(sc_service, self).start()
        sc.start(self.name)

    def stop(self):
        super(sc_service, self).stop()
        sc.stop(self.name)

    def create(self):
        super(sc_service, self).create()
        sc.create(
            self.name,
            self.params['executable'])

    def remove(self):
        super(sc_service, self).remove()
        sc.remove(self.name)

    def restart(self):
        super(sc_service, self).restart()
        self.stop()
        self.start()

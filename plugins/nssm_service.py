from .application_deployer import application_deployer
from .utils import chocolatey
from .utils import nssm

class nssm_service(application_deployer):

    def get_installed_version(self):
        super(nssm_service, self).get_installed_version()
        chocolatey.get_installed_version(self.pkg_name)

    def download(self):
        super(nssm_service, self).download()
        chocolatey.install(self.pkg_name, self.version,
                           source=self.global_config['choco_source'],
                           download_only=True)

    def configure(self):
        super(nssm_service, self).configure()
        self._copy_folder_templates(
            self.generic_config_path,
            '{0}/{1}'.format(self.install_path, 'Configs'),
            '*.config')
        self._copy_folder_templates(
            self.specific_config_path,
            '{0}/{1}'.format(self.install_path, 'Configs'),
            '*.config')

    def deploy(self):
        super(nssm_service, self).deploy()
        self.stop()
        self.remove()

        self.download()
        self._sync_folders(
            '{0}/{1}'.format(chocolatey.download_path, self.pkg_name),
            self.install_path)

        self.create()
        self.configure()

        self.start()

    def create(self):
        super(nssm_service, self).create()
        nssm.create(
            self.name,
            self.params['executable'],
            self.params['arguments'])

    def remove(self):
        super(nssm_service, self).remove()
        nssm.remove(self.name)

    def start(self):
        super(nssm_service, self).start()
        nssm.start(self.name)

    def stop(self):
        super(nssm_service, self).stop()
        nssm.stop(self.name)

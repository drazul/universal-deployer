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
                           source=self.global_config['choco_source']
                           if 'choco_source' in self.global_config
                           else None,
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

        nssm.set_delay_after_restart(self.name, 6000)  # 6 seconds
        nssm.set_stdout_log_file(
            self.name,
            'C:/var/log/{service_name}.stdout.log'.format(
                service_name=self.name))
        nssm.set_stderr_log_file(
            self.name,
            'C:/var/log/{service_name}.stderr.log'.format(
                service_name=self.name))
        nssm.set_log_rotation(self.name, 3145728, 86400)  # 3MB, 1 day

        if 'environment_file' in self.params:
            nssm.set_custom_environment_variables(
                self.name,
                self._get_file_lines_as_list('{0}/{1}'.format(
                    self.specific_config_path,
                    self.name + '.env'
                )))

    def deploy(self):
        super(nssm_service, self).deploy()
        self.stop()
        self.remove()

        self.download()
        self._sync_folders(
            '{0}/{1}/content'.format(chocolatey.download_path, self.pkg_name),
            self.install_path)

        self.create()
        self.configure()

        self.start()

    def create(self):
        super(nssm_service, self).create()
        nssm.create(
            self.name,
            '%s/%s' % (self.install_path, self.params['executable']),
            self.params['arguments']
            if 'arguments' in self.params else None)

    def remove(self):
        super(nssm_service, self).remove()
        nssm.remove(self.name)

    def start(self):
        super(nssm_service, self).start()
        nssm.start(self.name)

    def stop(self):
        super(nssm_service, self).stop()
        nssm.stop(self.name)

    def restart(self):
        super(nssm_service, self).restart()
        self.stop()
        self.start()

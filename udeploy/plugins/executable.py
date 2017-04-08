from .application_deployer import application_deployer
from .utils import chocolatey
from .utils import process


class executable(application_deployer):

    def get_installed_version(self):
        super(executable, self).get_installed_version()
        chocolatey.get_installed_version(self.pkg_name)

    def download(self):
        super(executable, self).download()
        chocolatey.install(self.pkg_name, self.version,
                           source=self.global_config['choco_source']
                           if 'choco_source' in self.global_config
                           else None,
                           download_only=True)

    def deploy_post(self):
        super(executable, self).deploy_post()
        cmd = '{executable} {arguments}'.format(
            executable=self.params['executable'],
            arguments=self.params['arguments']
        )

        process.execute(cmd)

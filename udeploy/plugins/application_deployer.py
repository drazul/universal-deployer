import fnmatch
import codecs
import glob
import os

import jinja2

from .utils import sync_folders

from logger import logger


class application_deployer(object):

    def __init__(
                self, name, app_config, app_type,
                weight, global_config, config_path, install_path):
        self.name = name
        self.app_config = app_config
        self.app_type = app_type
        self.weight = weight
        self.global_config = global_config
        self.version = app_config['version']
        self.pkg_name = app_config['pkg_name']
        self.params = app_config.get('params', None)

        self.generic_config_path = config_path
        self.specific_config_path = '{0}/{1}'.format(
            config_path, name)

        self.install_path = install_path

    def __str__(self):
        return '{weight} {app_name} {version}'.format(
            weight=self.weight,
            app_name=self.name, version=self.version)

    def str(self):
        logger.info(self)

    @staticmethod
    def _get_file_lines_as_list(filename):
        with open(filename) as f:
            content = f.readlines()
        return [x.strip() for x in content]

    @staticmethod
    def _sync_folders(src, dst):
        logger.debug('Moving data from {0} to {1}'.format(
            src, dst))
        sync_folders.sync(src, dst)

    @staticmethod
    def _replacement_list_on_file(filename, replacement_list):
        lines = []
        with open(filename) as infile:
            for line in infile:
                for old, new in replacement_list.items():
                    line = line.replace(old, new)
                lines.append(line)
        with open(filename, 'w') as outfile:
            for line in lines:
                outfile.write(line)

    @staticmethod
    def _find_files(root_path, pattern):
        file_list = []
        if not os.path.isdir(root_path):
            return file_list

        for file in os.listdir(root_path):
            if fnmatch.fnmatch(file, pattern):
                file_list.append(file)
        return file_list

    def _copy_folder_templates(self, src, dst, pattern):
        logger.debug('Configuring config templates from {0} to {1}'.format(
            src, dst))

        os.makedirs(dst, exist_ok=True)

        variables = {
            'app_name': self.name,
            'app_version': self.version,
            'environment': self.global_config['environmentname'],
            'log_levels':
                self.global_config['log_level']
                if 'log_level' in self.global_config else '',
        }

        files = glob.glob('{0}/{1}'.format(src, pattern))

        for f in files:
            path, filename = os.path.split(f)
            dst_file = '%s/%s' % (dst, filename)
            logger.debug('Rendering %s template into %s'
                         % (f, dst_file))
            content = jinja2.Environment(
                loader=jinja2.FileSystemLoader(path or './')
            ).get_template(filename).render(variables)
            with codecs.open(dst_file, 'w', 'utf-8') as f_dst:
                f_dst.write(content)

    def get_installed_version(self):
        # noinspection PyUnresolvedReferences
        if (self.get_installed_version.__code__ is not
                application_deployer.get_installed_version.__code__):
            logger.info('Task get_installed_version {0}'.format(self.name))

    def download(self):
        # noinspection PyUnresolvedReferences
        if (self.download.__code__ is not
                application_deployer.download.__code__):
            logger.info('Task download {0} version {1}'.format(
                self.pkg_name, self.version))

    def configure(self):
        # noinspection PyUnresolvedReferences
        if (self.configure.__code__ is not
                application_deployer.configure.__code__):
            logger.info('Task configure {0}'.format(self.name))

    def deploy_pre(self):
        # noinspection PyUnresolvedReferences
        if (self.deploy_pre.__code__ is not
                application_deployer.deploy_pre.__code__):
            logger.info('Task deploy_pre {0}'.format(self.name))

    def deploy(self):
        # noinspection PyUnresolvedReferences
        if (self.deploy.__code__ is not
                application_deployer.deploy.__code__):
            logger.info('Task deploy {0}'.format(self.name))

    def deploy_post(self):
        # noinspection PyUnresolvedReferences
        if (self.deploy_post.__code__ is not
                application_deployer.deploy_post.__code__):
            logger.info('Task deploy_post {0}'.format(self.name))

    def start(self):
        # noinspection PyUnresolvedReferences
        if (self.start.__code__ is not
                application_deployer.start.__code__):
            logger.info('Task start {0}'.format(self.name))

    def stop(self):
        # noinspection PyUnresolvedReferences
        if (self.stop.__code__ is not
                application_deployer.stop.__code__):
            logger.info('Task stop {0}'.format(self.name))

    def create(self):
        # noinspection PyUnresolvedReferences
        if (self.create.__code__ is not
                application_deployer.create.__code__):
            logger.info('Task create {0}'.format(self.name))

    def remove(self):
        # noinspection PyUnresolvedReferences
        if (self.remove.__code__ is not
                application_deployer.remove.__code__):
            logger.info('Task remove {0}'.format(self.name))

    def restart(self):
        # noinspection PyUnresolvedReferences
        if (self.restart.__code__ is not
                application_deployer.restart.__code__):
            logger.info('Task restart {0}'.format(self.name))

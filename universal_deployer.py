#!/usr/bin/env python3

import argparse
import os
import platform
import sys
import time
import zipfile

import yaml

from logger import logger
from logger import config_logger

from plugins.nssm_service import nssm_service
from plugins.sc_service import sc_service
from plugins.iis_website import iis_website
from plugins.curator import curator
from plugins.databases import databases
from plugins.executable import executable

__all__ = [nssm_service, sc_service, iis_website, curator, databases,
           executable, ]


class Deployer:
    def __init__(self, config_file, config_path, install_path):
        self.apps = []

        self.config_data = self._yaml2map(config_file)
        self.global_config = self.config_data['config']

        if self.global_config['config_path']:
            self.config_path = self.global_config['config_path']
        else:
            self.config_path = config_path

        if self.global_config['install_path']:
            self.install_path = self.global_config['install_path']
        else:
            self.install_path = install_path

        self._create_objects()
        self._order_objects_by_weight()

    @staticmethod
    def _str2class(class_name):
        try:
            return getattr(sys.modules[__name__], class_name)
        except:
            raise ValueError("Class %s not exists!" % class_name)

    @staticmethod
    def _str2method(class_name, method):
        try:
            return getattr(class_name, method)
        except:
            raise ValueError("Method %s not exists!" % method)

    @staticmethod
    def _yaml2map(filename):
        with open(filename, 'r') as stream:
            try:
                return yaml.load(stream)
            except yaml.YAMLError as error:
                logger.error('Error when load {0}\n {1}'.format(
                    filename, error))

    def backup(self, path):
        logger.info('Starting backup of {0}'.format(self.install_path))
        if not os.path.exists(path):
            os.makedirs(path)

        filename = '{0}/backup-{1}.zip'.format(
            path,
            time.strftime("%Y-%m-%d_%H:%M"))
        zipf = zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED)
        for root, dirs, files in os.walk(self.install_path):
            for file in files:
                absolute_path = os.path.join(root, file)
                zipf.write(
                    absolute_path,
                    absolute_path[len(self.install_path) + len(os.sep) - 1:])
        zipf.close()
        logger.info('Finished backup {0}'.format(filename))

    def _filter(self, app_filter):
        if app_filter == ['all']:
            return self.apps
        else:
            return [app for app in self.apps if app.app_type in app_filter]

    def _create_objects(self):
        for app_type, all_apps in self.config_data['apps'].items():
            try:
                class_type = self._str2class(app_type)
                weight = 0
                if 'weight' in self.global_config:
                    weight = self.global_config['weight']

                for app_name, app_config in all_apps.items():
                    if app_name == 'weight':
                        weight = app_config
                        continue

                    if 'weight' in app_config:
                        weight = app_config['weight']

                    self.apps.append(
                        class_type(
                            app_name, app_config,
                            app_type, weight,
                            self.global_config,
                            '{0}/{1}'.format(self.config_path, app_type),
                            '{0}/{1}/{2}'.format(
                                self.install_path,
                                app_type, app_name)))

            except ValueError as error:
                logger.warning(error)

    def _order_objects_by_weight(self):
        self.apps = sorted(self.apps, key=lambda app: app.weight, reverse=True)

    def execute(self, command, app_filter):
        logger.info('Executing task {command} {filter}'.format(
            command=command, filter=app_filter))
        app_filter = self._filter(app_filter)
        if command == 'str':
            logger.info('weight app_name version')
        for app in app_filter:
            self._str2method(app, command)()


if __name__ == "__main__":

    _is_windows = platform.system() is 'Windows'

    parser = argparse.ArgumentParser(description='Universal deployer')

    parser.add_argument('--log-file',
                        help='File where save the application log', type=str)
    parser.add_argument('--debug',
                        help='Debug log', action='store_true',
                        default=False)
    parser.add_argument('--quiet',
                        help='Silent log', action='store_true',
                        default=False)

    parser.add_argument('--list',
                        help='list apps by type or all',
                        nargs='*', type=str)

    parser.add_argument('--list-installed-versions',
                        help='Get installed version of each app',
                        type=str)

    parser.add_argument('--start',
                        help='start all apps, all by type or by name',
                        nargs='*', type=str)
    parser.add_argument('--stop',
                        help='stop all apps, all by type or by name',
                        nargs='*', type=str)
    parser.add_argument('--restart',
                        help='restart all apps, all by type or by name',
                        nargs='*', type=str)

    parser.add_argument('--deploy',
                        help='deploy all apps, all by type or by name',
                        nargs='*', type=str)
    parser.add_argument('--deploy-pre',
                        help='pre deploy all apps, all by type or by name',
                        nargs='*', type=str)
    parser.add_argument('--deploy-post',
                        help='post deploy all apps, all by type or by name',
                        nargs='*', type=str)

    parser.add_argument('--download',
                        help='download all apps, all by type or by name',
                        nargs='*', type=str)

    parser.add_argument('--configure',
                        help='configure all apps, all by type or by name',
                        nargs='*', type=str)

    parser.add_argument('--backup', help='Perform a backup of install path',
                        action='store_true', default=False)
    parser.add_argument('--backup-path',
                        help='path where store backup of old deployment',
                        type=str,
                        default='{0}/opt/universal-deployer-backups'.format(
                            'C:' if _is_windows else ''))

    parser.add_argument('--config-file',
                        help=('Contains apps to install with its version '
                              'number and parameters'),
                        type=str)
    parser.add_argument('--config-path',
                        help=('Folder that contains the configuration of apps'
                              ' to install. Default /etc/universal-deployer'),
                        type=str,
                        default='{0}/etc/universal-deployer'.format(
                            'C:' if _is_windows else ''))
    parser.add_argument('--install-path',
                        help=('Folder where will be installed all apps. '
                              'Default /opt/universal-deployer'),
                        type=str, default='{0}/opt/universal-deployer'.format(
                            'C:' if _is_windows else ''))

    args = parser.parse_args()

    if args.config_file is None:
        print('You need specify a valid config file.')
        sys.exit(-1)

    config_logger(args.log_file, args.debug, args.quiet)

    logger.info('Starting {project_name}'.format(
        project_name='universal_deployer'))

    deployer = Deployer(
        args.config_file,
        args.config_path if args.config_path is not None else None,
        args.install_path if args.install_path is not None else None)

    if args.backup:
        deployer.backup(args.backup_path)

    if args.list:
        deployer.execute('str', args.list)
    if args.list_installed_versions:
        deployer.execute('get_installed_versions', args.configure)
    if args.start:
        deployer.execute('start', args.start)
    if args.stop:
        deployer.execute('stop', args.stop)
    if args.restart:
        deployer.execute('restart', args.restart)
    if args.deploy:
        deployer.execute('deploy', args.deploy)
    if args.deploy_pre:
        deployer.execute('deploy_pre', args.deploy_pre)
    if args.deploy_post:
        deployer.execute('deploy_post', args.deploy_post)
    if args.download:
        deployer.execute('download', args.download)
    if args.configure:
        deployer.execute('configure', args.configure)

    logger.info('{project_name} finished successfully!'.format(
        project_name='universal_deployer'))

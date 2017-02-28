import logging

from .process import execute

__name__ = 'universal_deployer'
logger = logging.getLogger(__name__)


def create_database(db_server, db_name, changelog_file, properties_file):
    cmd = 'liquibase --changeLogFile={changelog_file} \
    --url="jdbc:sqlserver://{db_server};" --defaultsFile={properties_file} \
    update -DDATABASENAME={db_name}'.format(
        db_server=db_server, db_name=db_name, changelog_file=changelog_file,
        properties_file=properties_file)
    execute(cmd)


def update_database(db_server, db_name, changelog_file,
                    properties_file, params=None):

    cmd = 'liquibase --changeLogFile={changelog_file} \
    --url="jdbc:sqlserver://{db_server};database={db_name}" \
    --defaultsFile={properties_file} update {params}'.format(
        db_server=db_server, db_name=db_name, changelog_file=changelog_file,
        properties_file=properties_file, params=params)
    execute(cmd)


def update_database_context(db_server, db_name, changelog_file,
                            properties_file, contexts):

    cmd = 'liquibase --changeLogFile={changelog_file} \
    --url="jdbc:sqlserver://{db_server};database={db_name}" \
    --defaultsFile={properties_file} update --contexts={contexts}'.format(
        db_server=db_server, db_name=db_name, changelog_file=changelog_file,
        properties_file=properties_file, contexts=contexts)
    execute(cmd)

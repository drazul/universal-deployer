from .process import execute


def create_database(db_server, db_name, changelog_file, properties_file):
    cmd = ('liquibase --changeLogFile={changelog_file} '
           '--url="jdbc:sqlserver://{db_server};" '
           '--defaultsFile={properties_file} update '
           '-DDATABASENAME={db_name}').format(
        db_server=db_server, db_name=db_name, changelog_file=changelog_file,
        properties_file=properties_file)
    execute(cmd)


def update_database(db_server, db_name, changelog_file,
                    properties_file, arguments=None, contexts=None):

    cmd = ('liquibase --changeLogFile={changelog_file} '
           '--url="jdbc:sqlserver://{db_server};database={db_name}" '
           '--defaultsFile={properties_file} update').format(
        db_server=db_server, db_name=db_name, changelog_file=changelog_file,
        properties_file=properties_file, arguments=arguments)

    if arguments:
        cmd += ' {arguments}'.format(arguments=arguments)
    if contexts:
        cmd += ' --contexts={contexts}'.format(contexts=contexts)
    execute(cmd)

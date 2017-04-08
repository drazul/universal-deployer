from .process import execute

appcmd = 'C:/Windows/system32/inetsrv/appcmd.exe'


def start(name):
    cmd = '{appcmd} start site /site.name:{name}'.format(
            appcmd=appcmd, name=name)
    execute(cmd)


def stop(name):
    cmd = '{appcmd} stop site /site.name:{name}'.format(
            appcmd=appcmd, name=name)
    execute(cmd)


def configure_webconfig(working_dir, name, key, value):
    cmd = ('''{appcmd} set config {name} /section:appSettings '''
           '''/-"[key='{key}']"''').format(appcmd=appcmd, name=name, key=key)
    execute(cmd, working_directory=working_dir, ignore_errors=True)

    cmd = ('''{appcmd} set config {name} /section:appSettings '''
           '''/+"[key='{key}',value='{value}']"''').format(
            appcmd=appcmd, name=name, key=key, value=value)
    execute(cmd, working_directory=working_dir)


def configure(working_dir, name, start_mode, idle_timeout, ping_response_time,
              rapid_fail_protection, recycling_preriodic, recycling_schedule):
    cmd = '''{appcmd} set apppool
    /apppool.name: {name}
    /startmode:{start_mode}
    /processmodel.idletimeout:{idle_timeout}
    /processmodel.pingresponsetime:{ping_response_time}
    /failure.rapidfailprotection:"{rapid_fail_protection}"
    /recycling.periodicrestart.time:{recycling_preriodic}
    /+recycling.periodicRestart.schedule.[value='{recycling_schedule}']
    '''.format(
        appcmd=appcmd, name=name, start_mode=start_mode,
        idle_timeout=idle_timeout, ping_response_time=ping_response_time,
        rapid_fail_protection=rapid_fail_protection,
        recycling_preriodic=recycling_preriodic,
        recycling_schedule=recycling_schedule)
    execute(cmd, working_directory=working_dir)

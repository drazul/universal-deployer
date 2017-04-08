import subprocess
import sys

from logger import logger


def execute(command, ignore_errors=False):
    logger.debug('Executing: {0}'.format(command))

    proc = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True)

    stdout = list()
    stderr = list()
    while proc.poll() is None:
        while True:
            line = proc.stdout.readline()
            if not line:
                break
            stdout.append(line.decode('utf-8').replace(
                '\x00', '').replace('\r', '').replace('\n', ''))
            logger.info(stdout[-1])

        while True:
            line = proc.stderr.readline()
            if not line:
                break
            stderr.append(line.decode('utf-8').replace(
                '\x00', '').replace('\r', '').replace('\n', ''))
            logger.error(stderr[-1])

    result = dict(
        return_code=proc.returncode,
        stdout=stdout,
        stderr=stderr,
    )
    logger.debug(result)

    if not ignore_errors and result['return_code'] != 0:
        sys.exit(proc.returncode)

    return result

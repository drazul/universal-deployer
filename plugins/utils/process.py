import subprocess
import sys

from logger import logger


def execute(command, ignore_errors=True):
    logger.debug('Executing: {0}'.format(command))

    proc = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True)
    while proc.poll() is None:
        while True:
            line = proc.stdout.readline()
            if not line:
                break
            logger.info(line)

        while True:
            line = proc.stderr.readline()
            if not line:
                break
            logger.error(line)

    if ignore_errors:
        return proc.returncode

    if proc.returncode != 0:
        sys.exit(proc.returncode)

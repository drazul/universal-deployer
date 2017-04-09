import logging

TRACE = 5
logging.addLevelName(TRACE, "TRACE")
logger = logging.getLogger('universal_deployer')


def config_logger(log_file, debug, trace, quiet):
    if quiet:
        level = logging.FATAL
    else:
        if trace:
            level = TRACE
        elif debug:
            level = logging.DEBUG
        else:
            level = logging.INFO

    logger.setLevel(level)

    if log_file is not None:
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh = logging.FileHandler(log_file)
        fh.setFormatter(file_formatter)
        logger.addHandler(fh)

    console_formatter = logging.Formatter('%(levelname)s - %(message)s')
    ch = logging.StreamHandler()
    ch.setFormatter(console_formatter)
    logger.addHandler(ch)

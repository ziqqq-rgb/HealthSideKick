import logging

def setup_logger(name="HealthSideKick"):

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.hasHandlers():

        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "[%(asctime)s] - [%(levelname)s] - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger

logger = setup_logger()
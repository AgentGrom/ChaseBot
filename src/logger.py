import logging

def set_logger(name):
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    logging.getLogger("httpx").setLevel(logging.WARNING)
    logger = logging.getLogger(name)
    return logger
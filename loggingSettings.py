import logging.config
import pathlib
from portability import resource_path

def logger_initialization(log_name):
    """The function initialises a logger instance. And sets a logger 
    file.

    Args:
        log_name (str): Name of the logging file.
    """
    global logger

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(levelname)s: %(asctime)s: %(process)s: %(funcName)s: %(message)s')

    stream_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(pathlib.Path(
        resource_path(f'Settings/{log_name}')))
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger


def logger_wrapper(func):
    """The wrapper function handles logging information for
    fired functions.

    Args:
        func (function): Wrapped function.
    """
    def log_wrapper(*args):
        logger.info(f'{func.__name__} Section started.')
        try:
            result = func(*args)
        except Exception as e:
            logger.error(e)
        logger.info('Section ended.')
        
        return result
        
    return log_wrapper

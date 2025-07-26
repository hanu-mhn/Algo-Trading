import logging
import os

def setup_logger(name: str, log_file: str = "algo_trading.log", level=logging.INFO):
    os.makedirs("logs", exist_ok=True)
    log_path = os.path.join("logs", log_file)
    handler = logging.FileHandler(log_path)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s')
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.handlers:
        logger.addHandler(handler)
    return logger

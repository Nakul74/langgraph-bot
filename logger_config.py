from pathlib import Path
from loguru import logger

def get_logger(file_path):
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    logger.add(file_path, rotation="1 week", retention="10 days", level="INFO", catch=True, backtrace=True, diagnose=True)
    
    return logger
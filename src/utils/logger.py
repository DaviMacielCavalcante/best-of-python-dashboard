from loguru import logger
from pathlib import Path

logs_path = Path(__file__).parent.parent.parent/".temp"/"logs"

logger.add(sink=logs_path/"log_{time}.log", level="DEBUG", rotation="10 MB", retention="15 days")
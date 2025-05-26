# Version 1.5 (Modular - COPILOT - CHECKPOINT) 05.05 21:05 (Compatible with 1.5.1, 1.5.2, 1.5.3, 1.6, 1.6.1, 1.7, 1.8, 1.8.1, 1.9)

import logging
from logging.handlers import RotatingFileHandler

# Initialize the logger
LOG_FILE = "vm_manager.log"
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
LOG_LEVEL = logging.DEBUG

# Configure the logger
logger = logging.getLogger("VMManager")
logger.setLevel(LOG_LEVEL)

# File handler with log rotation
file_handler = RotatingFileHandler(LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=2)  # 5 MB per file, 2 backups
file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(LOG_FORMAT))

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)
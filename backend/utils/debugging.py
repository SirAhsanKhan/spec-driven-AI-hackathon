import sys
import os
import logging
from logging.handlers import RotatingFileHandler
from config import DATABASE_URL
import psutil
import time
from datetime import datetime

def setup_logging(log_level=logging.INFO, log_file="app.log"):
    """
    Setup comprehensive logging for the application
    """
    # Create logs directory if it doesn't exist
    logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    log_path = os.path.join(logs_dir, log_file)
    
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(log_level)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    
    # Create file handler with rotation
    file_handler = RotatingFileHandler(
        log_path,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

def log_system_info():
    """
    Log system information for debugging purposes
    """
    logger = logging.getLogger(__name__)
    
    logger.info(f"Application started at: {datetime.now()}")
    logger.info(f"Database URL: {DATABASE_URL}")
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Process ID: {os.getpid()}")
    
    # Log system resources
    process = psutil.Process(os.getpid())
    logger.info(f"Memory usage: {process.memory_info().rss / 1024 / 1024:.2f} MB")
    logger.info(f"CPU usage: {psutil.cpu_percent(interval=1)}%")

def debug_endpoint_info(app):
    """
    Log information about registered endpoints
    """
    logger = logging.getLogger(__name__)
    
    logger.info("Registered endpoints:")
    for route in app.routes:
        if hasattr(route, 'methods') and hasattr(route, 'path'):
            logger.info(f"  {', '.join(route.methods)} {route.path}")
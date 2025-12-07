import logging
from typing import Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class RAGException(Exception):
    """
    Custom exception class for RAG Chatbot application
    """
    def __init__(self, message: str, error_code: str = None, details: Any = None):
        self.message = message
        self.error_code = error_code
        self.details = details
        super().__init__(self.message)

    def __str__(self):
        if self.error_code:
            return f"[{self.error_code}] {self.message}"
        return self.message

def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the specified name
    """
    return logging.getLogger(name)
"""Sanitizing logging utility to prevent sensitive data leaks."""
import logging
import re

logger = logging.getLogger("doc_explainer")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s'))
if not logger.handlers:
    logger.addHandler(handler)

def sanitize(text: str) -> str:
    """Masks credit card numbers and account patterns."""
    return re.sub(r'\b\d{4}[ -]?\d{4}[ -]?\d{4}[ -]?\d{4}\b', '****-****-****-****', str(text))

def log_info(msg: str):
    logger.info(sanitize(msg))

def log_error(msg: str):
    logger.error(sanitize(msg))
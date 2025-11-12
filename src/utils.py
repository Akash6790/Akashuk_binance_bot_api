"""utils.py
Utility functions: validator, logger setup, and client factory for Binance testnet.
"""
import os, logging

LOG_FILE = os.path.join(os.path.dirname(__file__), '..', 'bot.log')

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    # avoid duplicate handlers
    if not logger.handlers:
        fh = logging.FileHandler(LOG_FILE)
        fh.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        # also console
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    return logger

def create_client(api_key: str, api_secret: str, testnet: bool = True):
    try:
        from binance.client import Client
    except Exception:
        try:
            from binance import Client
        except Exception:
            Client = None
    if Client is None:
        raise RuntimeError('python-binance library not installed. Install with: pip install python-binance')
    client = Client(api_key, api_secret)
    if testnet:
        # configure testnet base URL for futures
        client.FUTURES_URL = 'https://testnet.binancefuture.com'
    return client

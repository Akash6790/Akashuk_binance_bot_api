"""market_orders.py
Simple market order placement for Binance USDT-M Futures (testnet).
"""
import logging
import time
from typing import Dict, Any

try:
    # python-binance library import (two common styles)
    from binance.client import Client
except Exception:
    try:
        from binance import Client
    except Exception:
        Client = None  # library not installed; code will raise if used without it

logger = logging.getLogger(__name__)

def place_market_order(client, symbol: str, side: str, quantity: float, recv_window: int = 5000) -> Dict[str, Any]:
    """Place a market order on USDT-M Futures testnet.

    Args:
        client: authenticated Binance Client configured for futures testnet.
        symbol: trading pair (e.g., 'BTCUSDT')
        side: 'BUY' or 'SELL'
        quantity: quantity to trade (in contract quantity for futures)
    Returns:
        API response as dict.
    """
    assert side.upper() in ("BUY", "SELL"), "side must be BUY or SELL"
    if Client is None:
        raise RuntimeError("python-binance not installed in this environment.")
    logger.info(f"Placing market order: {symbol} {side} {quantity}")
    try:
        # futures_create_order for USDT-M Futures via python-binance
        resp = client.futures_create_order(
            symbol=symbol.upper(),
            side=side.upper(),
            type='MARKET',
            quantity=quantity,
            recvWindow=recv_window
        )
        logger.info(f"Order response: {resp}")
        return resp
    except Exception as e:
        logger.exception("Failed to place market order")
        raise

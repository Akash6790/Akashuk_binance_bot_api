"""limit_orders.py
Simple limit order placement for Binance USDT-M Futures (testnet).
"""
import logging
from typing import Dict, Any

try:
    from binance.client import Client
except Exception:
    try:
        from binance import Client
    except Exception:
        Client = None

logger = logging.getLogger(__name__)

def place_limit_order(client, symbol: str, side: str, quantity: float, price: float, time_in_force: str = 'GTC') -> Dict[str, Any]:
    assert side.upper() in ("BUY", "SELL"), "side must be BUY or SELL"
    if Client is None:
        raise RuntimeError("python-binance not installed in this environment.")
    logger.info(f"Placing limit order: {symbol} {side} {quantity} @ {price}")
    try:
        resp = client.futures_create_order(
            symbol=symbol.upper(),
            side=side.upper(),
            type='LIMIT',
            price=str(price),
            quantity=quantity,
            timeInForce=time_in_force
        )
        logger.info(f"Order response: {resp}")
        return resp
    except Exception as e:
        logger.exception("Failed to place limit order")
        raise

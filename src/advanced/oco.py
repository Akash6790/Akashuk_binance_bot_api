"""oco.py
Simulated OCO (One-Cancels-the-Other) for futures by placing two orders and cancelling the other when one fills.
NOTE: Binance Futures API does not support classic OCO in the same way as Spot API.
This module provides a simple implementation pattern using polling. Use carefully on TESTNET.
"""
import logging, time
from typing import Dict, Any

logger = logging.getLogger(__name__)

def place_oco_simulated(client, symbol: str, side: str, quantity: float, take_profit_price: float, stop_price: float, stop_limit_price: float = None, poll_interval: float = 2.0):
    """Place two orders: take-profit (LIMIT) and stop (LIMIT or STOP_MARKET). When one is filled, cancel the other.

    Returns both order infos as dicts.
    """
    side = side.upper()
    assert side in ("BUY", "SELL"), "side must be BUY or SELL"
    # Decide stop order type if stop_limit_price provided then STOP, else STOP_MARKET
    stop_order_type = 'STOP' if stop_limit_price is not None else 'STOP_MARKET'
    tp_side = 'SELL' if side == 'BUY' else 'BUY'

    # Place TP order
    logger.info("Placing take-profit order (limit)")
    tp = client.futures_create_order(
        symbol=symbol,
        side=tp_side,
        type='LIMIT',
        price=str(take_profit_price),
        quantity=quantity,
        timeInForce='GTC'
    )

    # Place stop order
    logger.info("Placing stop order")

    if stop_order_type == 'STOP':
        stop = client.futures_create_order(
            symbol=symbol,
            side=tp_side,
            type='STOP',
            stopPrice=str(stop_price),
            price=str(stop_limit_price),
            quantity=quantity,
            timeInForce='GTC'
        )
    else:
        stop = client.futures_create_order(
            symbol=symbol,
            side=tp_side,
            type='STOP_MARKET',
            stopPrice=str(stop_price),
            quantity=quantity
        )

    logger.info(f"TP order: {tp}")
    logger.info(f"Stop order: {stop}")

    # Poll orders: if one filled, cancel the other
    tp_id = tp.get('orderId')
    stop_id = stop.get('orderId')
    while True:
        time.sleep(poll_interval)
        tp_status = client.futures_get_order(symbol=symbol, orderId=tp_id)
        stop_status = client.futures_get_order(symbol=symbol, orderId=stop_id)
        logger.info(f"TP status: {tp_status.get('status')}, Stop status: {stop_status.get('status')}")
        if tp_status.get('status') == 'FILLED' and stop_status.get('status') not in ('CANCELED','FILLED'):
            client.futures_cancel_order(symbol=symbol, orderId=stop_id)
            logger.info('TP filled — canceled stop')
            break
        if stop_status.get('status') == 'FILLED' and tp_status.get('status') not in ('CANCELED','FILLED'):
            client.futures_cancel_order(symbol=symbol, orderId=tp_id)
            logger.info('Stop filled — canceled TP')
            break
    return { 'tp': tp_status, 'stop': stop_status }

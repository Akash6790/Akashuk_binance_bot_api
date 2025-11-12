"""twap.py
Simple TWAP implementation: splits a large order into N equal-sized market orders executed over a specified duration.
"""
import time, logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

def execute_twap(client, symbol: str, side: str, total_quantity: float, slices: int, duration_seconds: int):
    assert slices >= 1
    qty_per_slice = total_quantity / slices
    interval = duration_seconds / slices
    results: List[Dict[str, Any]] = []
    for i in range(slices):
        logger.info(f"TWAP slice {i+1}/{slices}: placing market order of {qty_per_slice}")
        resp = client.futures_create_order(
            symbol=symbol,
            side=side.upper(),
            type='MARKET',
            quantity=qty_per_slice
        )
        results.append(resp)
        time.sleep(interval)
    return results

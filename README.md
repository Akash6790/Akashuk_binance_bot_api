# Binance Futures Order Bot (Testnet)
**Author:** Akash u k


## Overview

This CLI-based bot demonstrates how to place Market and Limit orders on Binance USDT-M Futures Testnet.
It includes optional advanced strategies: a simulated OCO and a TWAP executor.

## Structure

Akash_u_k_binance_bot/
├── src/
│   ├── market_orders.py
│   ├── limit_orders.py
│   ├── utils.py
│   ├── cli.py
│   └── advanced/
│       ├── oco.py
│       └── twap.py
├── bot.log
├── report.pdf
└── README.md

## Setup

1. Create a Python 3.9+ virtual environment and activate it.
2. Install dependencies:
   ```bash
   pip install python-binance
   ```
3. Export your testnet API credentials or enter them at the prompt:
   ```bash
   export BINANCE_API_KEY=your_testnet_api_key
   export BINANCE_API_SECRET=your_testnet_api_secret
   ```

## Usage Examples

Place a market order:
```bash
python src/cli.py market --symbol BTCUSDT --side BUY --quantity 0.001
```

Place a limit order:
```bash
python src/cli.py limit --symbol BTCUSDT --side SELL --quantity 0.001 --price 65000
```

Run a TWAP:
```bash
python src/cli.py twap --symbol BTCUSDT --side BUY --quantity 0.01 --slices 5 --duration 300
```

Simulated OCO:
```bash
python src/cli.py oco --symbol BTCUSDT --side BUY --quantity 0.001 --tp 70000 --stop 58000
```

## Logging

All actions, API requests, responses and errors are logged to `bot.log` at the project root.

## Notes and Limitations

- This project uses the python-binance client; ensure it's installed.
- OCO is simulated because Binance Futures does not have the same OCO endpoint as Spot. The implementation provided polls order status and cancels the counterpart when one side fills — this is an example pattern for educational purposes.
- Always test on Testnet (https://testnet.binancefuture.com) before using real funds.

## Files to submit

- src/ (source code)
- bot.log
- report.pdf (this repo contains a basic report stub)
- README.md

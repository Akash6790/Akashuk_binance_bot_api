# 🚀 Akash u K -Binance Futures Order Bot (USDT-M Testnet)

**Author:** Akash U K  
**Type:** CLI-based Trading Bot for Binance USDT-M Futures  
**Mode:** Testnet Only — Safe for learning and experimentation  

---

## 📁 Project Folder Structure

```
Akash_u_k_binance_bot/
│
├── src/                            # All source code files
│   ├── cli.py                      # Main command-line interface for running the bot
│   ├── utils.py                    # Utilities for credentials, logging, and Binance client creation
│   ├── market_orders.py            # Logic for market orders
│   ├── limit_orders.py             # Logic for limit orders
│   ├── advanced/                   # Advanced order strategies
│   │   ├── oco.py                  # Simulated One-Cancels-the-Other (TP + Stop-loss)
│   │   └── twap.py                 # TWAP (Time Weighted Average Price) strategy
│
├── bot.log                         # Central log file (records every order & error)
├── report.pdf                      # Project analysis report (placeholder – add screenshots & observations)
└── README.md                       # Documentation and usage guide (this file)
```

---

## ⚙️ Requirements

| Requirement | Version | Description |
|--------------|----------|-------------|
| Python | 3.9+ | Required language environment |
| Library | `python-binance` | Official Binance Python API |
| Library | `python-dotenv` | For loading `.env` files automatically |
| Network | Internet access | Needed for connecting to Binance Futures Testnet |

Install dependencies:

```bash
pip install python-binance python-dotenv
```

---

## 🧠 Setup Instructions

### 1️⃣ Get Binance Futures Testnet API Keys
- Register at **[https://testnet.binancefuture.com](https://testnet.binancefuture.com)**
- Create **API Key** and **Secret Key** for testnet.

### 2️⃣ Save your credentials (once)
You can save your credentials permanently so you don’t re-enter them every time:

```bash
python src/cli.py --save-creds market --symbol BTCUSDT --side BUY --quantity 0.001
```
This will:
- Prompt for API key and secret once
- Save them in a secure file:  
  `C:\Users\<you>\.binance_bot\credentials.json`  
- Reuse them automatically for future runs.

---

## 🧩 Features

| Feature | Description |
|----------|-------------|
| 🟢 **Market Orders** | Instant execution at market price |
| 🔵 **Limit Orders** | Place a limit order at a specific price |
| 🟠 **TWAP Orders** | Splits a large order into smaller time-based slices |
| 🔴 **OCO Orders** | Simulated One-Cancels-the-Other (take-profit + stop-loss) |
| 🧾 **Logging** | All orders, responses, and errors logged to `bot.log` |
| ⚙️ **Validation** | Checks input validity, testnet connectivity, and API responses |
| 🔐 **Secure API Handling** | API credentials auto-saved (encrypted permissions 600) |
| 🧰 **Extensible Design** | Easy to add new strategies in `src/advanced/` |

---

## 🚀 Running the Bot

Each command runs through the main CLI interface:  
`python src/cli.py <command> [options]`

---

### 🟢 1. Market Order

Instantly buys/sells a contract at the market price.

```bash
python src/cli.py market --symbol BTCUSDT --side BUY --quantity 0.001
```

**Example Output:**
```
Market order placed:
{'orderId': 9563549807, 'symbol': 'BTCUSDT', 'status': 'NEW', 'type': 'MARKET', 'side': 'BUY', 'origQty': '0.001', 'executedQty': '0.000', 'updateTime': 1762942435116}
```

**How to analyze:**
- `status`: `NEW` → order accepted, may fill in a few ms.
- `executedQty`: amount filled (e.g., `0.000` → not filled yet).
- `orderId`: unique identifier (use it to check later).

---

### 🔵 2. Limit Order

Places a buy/sell order at a fixed price.

```bash
python src/cli.py limit --symbol BTCUSDT --side SELL --quantity 0.001 --price 106500
```

**Example Output:**
```
Limit order placed:
{'orderId': 9563550002, 'symbol': 'BTCUSDT', 'status': 'NEW', 'price': '106500.00', 'type': 'LIMIT'}
```

**How to analyze:**
- `status: NEW` → waiting to fill.
- `price`: confirms limit level.
- `type`: confirms correct order type.
- To cancel, use the order ID from the console or bot.log with Binance Testnet dashboard.

---

### 🟠 3. TWAP (Time-Weighted Average Price)

Splits a large order into smaller parts over time to avoid slippage.

```bash
python src/cli.py twap --symbol BTCUSDT --side BUY --quantity 0.01 --slices 5 --duration 300
```

- Splits `0.01` BTC into `5` slices = `0.002` BTC each.
- Executes one every `60s` (`300 / 5`).

**Example Output:**
```
TWAP slice 1/5: placing market order of 0.002
TWAP slice 2/5: placing market order of 0.002
...
TWAP executed, slice responses:
[{'orderId': ...}, {'orderId': ...}, ...]
```

**How to analyze:**
- Each slice’s `orderId` is logged.
- You can check fills individually.
- Use `Ctrl + C` anytime to stop midway safely.

---

### 🔴 4. OCO (One-Cancels-the-Other)

Simulates a Take-Profit and Stop-Loss simultaneously for a position.

```bash
python src/cli.py oco --symbol BTCUSDT --side BUY --quantity 0.001 --tp 106500 --stop 102500 --max-wait 60
```

**Example Output:**
```
INFO advanced.oco - Current market/mark price: 104654.23
INFO advanced.oco - Placing take-profit order (limit)
INFO advanced.oco - Placing stop order
INFO advanced.oco - TP order raw: {...}
INFO advanced.oco - Stop order raw: {...}
TP status: NEW, Stop status: NEW
```

**How to analyze:**
- `TP` (take-profit) and `Stop` are both active.
- When one fills, the other is canceled automatically.
- If `max-wait` expires, both remain active for manual cancellation.

🧠 **Important Rule:**  
For a **BUY (long)** position:
- TP must be **above** current price.  
- Stop must be **below** current price.  

For a **SELL (short)** position, reverse the rule.

---

### 🧾 5. Logs and Debugging

Every run automatically logs all actions to `bot.log`.

**Example log entries:**
```
2025-11-12 15:45:06,820 INFO root - Loaded API credentials
2025-11-12 15:45:10,549 INFO utils - futures_ping() succeeded
2025-11-12 15:45:10,549 INFO advanced.oco - Placing take-profit order (limit)
2025-11-12 15:45:11,000 INFO advanced.oco - TP order raw: {...}
```

**Tips:**
- Check `bot.log` for any exceptions.
- If you see `APIError(code=-4024)`, your TP/Stop are outside the allowed range — adjust them relative to the current mark price.

---

## 🧩 Notes & Recommendations

- Always test with **small quantities** on **Testnet**.
- Never use mainnet keys in this project.
- Binance Futures uses **contract price**, not spot price.
- All responses and timestamps are UTC-based.

---

**📜 Author:** Akash U K  
**🧠 Purpose:** Educational — backend trading bot design & API integration demo  
**🔗 Testnet URL:** [https://testnet.binancefuture.com](https://testnet.binancefuture.com)

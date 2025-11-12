"""cli.py
Command-line interface for the Binance Futures bot.
Usage examples (interactive prompts will request API keys):
    python cli.py market --symbol BTCUSDT --side BUY --quantity 0.001
    python cli.py limit --symbol BTCUSDT --side SELL --quantity 0.001 --price 60000
    python cli.py twap --symbol BTCUSDT --side BUY --quantity 0.01 --slices 5 --duration 300
"""

import argparse, os
from utils import setup_logging, create_client
from market_orders import place_market_order
from limit_orders import place_limit_order
from advanced.twap import execute_twap
from advanced.oco import place_oco_simulated

setup_logging()

def main():
    parser = argparse.ArgumentParser(description='Binance USDT-M Futures Order Bot (Testnet)')
    sub = parser.add_subparsers(dest='cmd')

    p_market = sub.add_parser('market')
    p_market.add_argument('--symbol', required=True)
    p_market.add_argument('--side', required=True, choices=['BUY','SELL'])
    p_market.add_argument('--quantity', type=float, required=True)

    p_limit = sub.add_parser('limit')
    p_limit.add_argument('--symbol', required=True)
    p_limit.add_argument('--side', required=True, choices=['BUY','SELL'])
    p_limit.add_argument('--quantity', type=float, required=True)
    p_limit.add_argument('--price', type=float, required=True)

    p_twap = sub.add_parser('twap')
    p_twap.add_argument('--symbol', required=True)
    p_twap.add_argument('--side', required=True, choices=['BUY','SELL'])
    p_twap.add_argument('--quantity', type=float, required=True)
    p_twap.add_argument('--slices', type=int, default=5)
    p_twap.add_argument('--duration', type=int, default=300, help='duration in seconds')

    p_oco = sub.add_parser('oco')
    p_oco.add_argument('--symbol', required=True)
    p_oco.add_argument('--side', required=True, choices=['BUY','SELL'])
    p_oco.add_argument('--quantity', type=float, required=True)
    p_oco.add_argument('--tp', type=float, required=True, help='take profit price')
    p_oco.add_argument('--stop', type=float, required=True, help='stop trigger price')
    p_oco.add_argument('--stop_limit', type=float, default=None, help='stop limit price (optional)')

    args = parser.parse_args()

    api_key = os.environ.get('BINANCE_API_KEY') or input('Enter API Key: ').strip()
    api_secret = os.environ.get('BINANCE_API_SECRET') or input('Enter API Secret: ').strip()
    client = create_client(api_key, api_secret, testnet=True)

    if args.cmd == 'market':
        resp = place_market_order(client, args.symbol, args.side, args.quantity)
        print('Market order placed:')
        print(resp)
    elif args.cmd == 'limit':
        resp = place_limit_order(client, args.symbol, args.side, args.quantity, args.price)
        print('Limit order placed:')
        print(resp)
    elif args.cmd == 'twap':
        resp = execute_twap(client, args.symbol, args.side, args.quantity, args.slices, args.duration)
        print('TWAP executed, slice responses:')
        print(resp)
    elif args.cmd == 'oco':
        resp = place_oco_simulated(client, args.symbol, args.side, args.quantity, args.tp, args.stop, args.stop_limit)
        print('OCO simulated result:')
        print(resp)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()

import yfinance as yf
from tabulate import tabulate

# Portfolio structure: { 'TICKER': {'quantity': int, 'buy_price': float} }
portfolio = {}

def add_stock(ticker, quantity, buy_price):
    ticker = ticker.upper()
    if ticker in portfolio:
        portfolio[ticker]['quantity'] += quantity
    else:
        portfolio[ticker] = {'quantity': quantity, 'buy_price': buy_price}
    print(f"Added {quantity} shares of {ticker} at ₹{buy_price:.2f}")

def remove_stock(ticker):
    ticker = ticker.upper()
    if ticker in portfolio:
        del portfolio[ticker]
        print(f"Removed {ticker} from portfolio.")
    else:
        print(f"{ticker} not found in portfolio.")

def get_stock_price(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period="1d")
    if not data.empty:
        return data['Close'].iloc[-1]
    return None

def view_portfolio():
    if not portfolio:
        print("Your portfolio is empty.")
        return

    table = []
    total_value = 0
    total_cost = 0

    for ticker, data in portfolio.items():
        current_price = get_stock_price(ticker)
        if current_price is None:
            print(f"Could not fetch data for {ticker}")
            continue

        quantity = data['quantity']
        buy_price = data['buy_price']
        current_value = current_price * quantity
        invested_value = buy_price * quantity
        profit_loss = current_value - invested_value
        profit_percent = (profit_loss / invested_value) * 100

        total_value += current_value
        total_cost += invested_value

        table.append([
            ticker,
            quantity,
            f"₹{buy_price:.2f}",
            f"₹{current_price:.2f}",
            f"₹{current_value:.2f}",
            f"₹{profit_loss:.2f}",
            f"{profit_percent:.2f}%"
        ])

    print(tabulate(table, headers=["Ticker", "Qty", "Buy Price", "Current Price", "Current Value", "P/L", "% Change"]))
    print(f"\nTotal Invested: ₹{total_cost:.2f}")
    print(f"Current Portfolio Value: ₹{total_value:.2f}")
    print(f"Total P/L: ₹{(total_value - total_cost):.2f}")

# Example usage
add_stock('AAPL', 10, 1500)
add_stock('GOOGL', 5, 2800)
view_portfolio()
remove_stock('AAPL')

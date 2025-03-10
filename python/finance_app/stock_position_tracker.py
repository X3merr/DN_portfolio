import yfinance as yf
import pandas as pd
from datetime import datetime

def fetch_stock_details_by_ticker(ticker):
    try:
        stock = yf.Ticker(ticker)
        history = stock.history(period='1d')
        if history.empty:
            print(f"No price data found for ticker {ticker}")
            return None, None, None
        currency = stock.info.get('currency', 'N/A')
        isin = stock.info.get('isin', 'N/A')
        return history['Close'].iloc[-1], currency, isin
    except Exception as e:
        print(f"Error fetching data for ticker {ticker}: {e}")
        return None, None, None

def add_stock_position(position_file):
    ticker = input("Enter Ticker: ")
    try:
        quantity = int(input("Enter quantity: "))
    except ValueError:
        print("Invalid input for quantity. Please enter a valid number.")
        return
    
    try:
        buy_price = float(input("Enter buy price: "))
    except ValueError:
        print("Invalid input for buy price. Please enter a valid number.")
        return
    
    currency = input("Enter currency: ")
    date = input("Enter purchase date (DD-MM-YYYY): ")
    
    try:
        datetime.strptime(date, "%d-%m-%Y")
    except ValueError:
        print("Invalid date format. Please use DD-MM-YYYY.")
        return
    
    current_price, _, isin = fetch_stock_details_by_ticker(ticker)
    
    new_data = pd.DataFrame([[ticker, isin, quantity, buy_price, currency, date]], 
                             columns=["Ticker", "ISIN", "Quantity", "Buy Price", "Currency", "Date"])
    
    try:
        df = pd.read_csv(position_file)
        df = pd.concat([df, new_data], ignore_index=True)
    except FileNotFoundError:
        df = new_data
    
    df.to_csv(position_file, index=False)
    print("Stock position added successfully.")

def check_stock_positions(position_file):
    try:
        df = pd.read_csv(position_file)
    except FileNotFoundError:
        print("Position file not found. Please provide a valid file.")
        return
    
    df[['Current Price', 'Currency', 'ISIN']] = df['Ticker'].apply(lambda x: pd.Series(fetch_stock_details_by_ticker(x)))
    df['Current Value'] = df['Current Price'] * df['Quantity']
    df['Profit/Loss'] = (df['Current Price'] - df['Buy Price']) * df['Quantity']
    df['Profit %'] = ((df['Current Price'] - df['Buy Price']) / df['Buy Price']) * 100
    
    aggregated = df.groupby("Ticker").agg({
        "Quantity": "sum", 
        "Buy Price": "mean", 
        "Current Price": "first",
        "Current Value": "sum", 
        "Profit/Loss": "sum",
        "Profit %": "mean",
        "Currency": "first",
        "ISIN": "first"
    }).reset_index()
    
    final_report = pd.DataFrame()
    for ticker in aggregated['Ticker'].unique():
        total_row = aggregated[aggregated['Ticker'] == ticker]
        detail_rows = df[df['Ticker'] == ticker]
        final_report = pd.concat([final_report, total_row, detail_rows], ignore_index=True, sort=False)
    
    print("Final Report:")
    print(final_report)
    
    final_report.to_csv("stock_positions_final_report.csv", index=False)
    print("Updated stock positions saved to stock_positions_final_report.csv")

if __name__ == "__main__":
    position_file = "stock_positions.csv"
    while True:
        choice = input("Choose an option: \n1. Add Stock Position\n2. Check Stock Positions\n3. Exit\nEnter choice: ")
        if choice == "1":
            add_stock_position(position_file)
        elif choice == "2":
            check_stock_positions(position_file)
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

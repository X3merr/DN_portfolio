import yfinance as yf
import pandas as pd
from datetime import datetime

def fetch_stock_price_by_isin(isin):
    try:
        stock = yf.Ticker(isin)
        history = stock.history(period='1d')
        if history.empty:
            print(f"No price data found for ISIN {isin}")
            return None
        return history['Close'].iloc[-1]
    except Exception as e:
        print(f"Error fetching price for ISIN {isin}: {e}")
        return None

def add_stock_position(position_file):
    isin = input("Enter ISIN: ")
    quantity = int(input("Enter quantity: "))
    buy_price = float(input("Enter buy price: "))
    date = input("Enter purchase date (YYYY-MM-DD): ")
    
    # Validate date format
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return
    
    new_data = pd.DataFrame([[isin, quantity, buy_price, date]], 
                             columns=["ISIN", "Quantity", "Buy Price", "Date"])
    
    try:
        df = pd.read_csv(position_file)
        df = pd.concat([df, new_data], ignore_index=True)
    except FileNotFoundError:
        df = new_data
    
    df.to_csv(position_file, index=False)
    print("Stock position added successfully.")

def check_stock_positions(position_file):
    # Load stock positions from CSV
    try:
        df = pd.read_csv(position_file)
    except FileNotFoundError:
        print("Position file not found. Please provide a valid file.")
        return
    
    df['Current Price'] = df['ISIN'].apply(fetch_stock_price_by_isin)
    df['Current Value'] = df['Current Price'] * df['Quantity']
    df['Profit/Loss'] = (df['Current Price'] - df['Buy Price']) * df['Quantity']
    
    print(df)
    
    # Save updated report
    df.to_csv("stock_positions_report.csv", index=False)
    print("Updated stock positions saved to stock_positions_report.csv")

if __name__ == "__main__":
    position_file = "stock_positions.csv"  # Ensure this file exists with columns: ISIN, Quantity, Buy Price, Date
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

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
        company_name = stock.info.get('shortName', 'N/A')
        return history['Close'].iloc[-1], currency, company_name
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
    
    current_price, _, company_name = fetch_stock_details_by_ticker(ticker)
    
    new_data = pd.DataFrame([[ticker, company_name, quantity, buy_price, currency, date]], 
                             columns=["Ticker", "Company Name", "Quantity", "Buy Price", "Currency", "Date"])
    
    try:
        df = pd.read_csv(position_file)
        df = pd.concat([df, new_data], ignore_index=True)
    except FileNotFoundError:
        df = new_data
    
    df.to_csv(position_file, index=False)
    print("Stock position added successfully.")

def remove_stock_position(position_file):
    try:
        df = pd.read_csv(position_file)
    except FileNotFoundError:
        print("Position file not found. Please provide a valid file.")
        return
    
    ticker = input("Enter the ticker to sell: ")
    try:
        sell_quantity = int(input("Enter quantity to sell: "))
        sell_price = float(input("Enter sell price: "))
    except ValueError:
        print("Invalid input. Please enter valid numbers.")
        return
    
    sell_date = input("Enter sale date (DD-MM-YYYY): ")
    try:
        datetime.strptime(sell_date, "%d-%m-%Y")
    except ValueError:
        print("Invalid date format. Please use DD-MM-YYYY.")
        return
    
    if ticker not in df['Ticker'].values:
        print("Stock not found in portfolio.")
        return
    
    company_name = df[df["Ticker"] == ticker]["Company Name"].values[0]
    currency_value = df[df["Ticker"] == ticker]["Currency"].values[0]
    
    new_data = pd.DataFrame([[ticker, company_name, -sell_quantity, sell_price, currency_value, sell_date]], 
                             columns=["Ticker", "Company Name", "Quantity", "Buy Price", "Currency", "Date"])
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(position_file, index=False)
    print("Stock sale recorded successfully.")

def check_stock_positions(position_file):
    try:
        df = pd.read_csv(position_file)
    except FileNotFoundError:
        print("Position file not found. Please provide a valid file.")
        return
    
    df[['Current Price', 'Currency', 'Company Name']] = df['Ticker'].apply(lambda x: pd.Series(fetch_stock_details_by_ticker(x)))
    df['Current Value'] = df['Current Price'] * df['Quantity']
    
    df = df.sort_values(by=['Date'], ascending=True)
    df['Profit/Loss'] = 0
    df['Profit %'] = 0
    
    fifo_queue = []
    for index, row in df.iterrows():
        if row['Quantity'] > 0:
            fifo_queue.append((row['Quantity'], row['Buy Price']))
        elif row['Quantity'] < 0:
            sell_quantity = abs(row['Quantity'])
            total_profit = 0
            original_quantity = sell_quantity
            
            while sell_quantity > 0 and fifo_queue:
                buy_quantity, buy_price = fifo_queue.pop(0)
                if buy_quantity > sell_quantity:
                    fifo_queue.insert(0, (buy_quantity - sell_quantity, buy_price))
                    buy_quantity = sell_quantity
                
                profit = (row['Buy Price'] - buy_price) * buy_quantity
                total_profit += profit
                sell_quantity -= buy_quantity
            
            df.at[index, 'Profit/Loss'] = total_profit
            df.at[index, 'Profit %'] = (total_profit / (original_quantity * buy_price)) * 100 if original_quantity * buy_price > 0 else 0
    
    total_summary = df.groupby('Ticker').agg(
        Total_Quantity=('Quantity', 'sum'),
        Total_Current_Value=('Current Value', 'sum')
    ).reset_index()
    
    print("Stock Positions:")
    print(df)
    print("\nTotal Summary for Each Stock:")
    print(total_summary)

def main():
    position_file = "stock_positions.csv"
    while True:
        print("\n1. Add Stock Position")
        print("2. Remove Stock Position")
        print("3. Check Stock Positions")
        print("4. Exit")
        choice = input("Choose an option: ")
        
        if choice == '1':
            add_stock_position(position_file)
        elif choice == '2':
            remove_stock_position(position_file)
        elif choice == '3':
            check_stock_positions(position_file)
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()

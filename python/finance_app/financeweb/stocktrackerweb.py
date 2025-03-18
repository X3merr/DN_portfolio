import yfinance as yf
import pandas as pd
import sqlite3
import redis
import json
from datetime import datetime
from flask import Flask, request, jsonify

# Database and Redis Cache Configuration
db_file = "stock_positions.db"
redis_client = redis.Redis(host='localhost', port=6379, db=0)
CACHE_EXPIRY = 900  # 15 minutes

app = Flask(__name__)

def init_db():
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS positions (
                            id INTEGER PRIMARY KEY,
                            ticker TEXT,
                            company_name TEXT,
                            quantity INTEGER,
                            buy_price REAL,
                            currency TEXT,
                            date TEXT)
                        ''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                            id INTEGER PRIMARY KEY,
                            ticker TEXT,
                            quantity INTEGER,
                            sell_price REAL,
                            date TEXT,
                            profit_loss REAL)
                        ''')
        conn.commit()

# Fetch stock details from Yahoo Finance with caching
@app.route("/fetch_stock/<ticker>", methods=["GET"])
def fetch_stock_details(ticker):
    cached_data = redis_client.get(f"stock:{ticker}")
    if cached_data:
        return jsonify(json.loads(cached_data))
    
    try:
        stock = yf.Ticker(ticker)
        history = stock.history(period='1d')
        if history.empty:
            return jsonify({"error": "No data found for ticker."}), 404
        
        currency = stock.info.get('currency', 'N/A')
        company_name = stock.info.get('shortName', 'N/A')
        close_price = history['Close'].iloc[-1]
        
        stock_data = {"price": close_price, "currency": currency, "company_name": company_name}
        redis_client.setex(f"stock:{ticker}", CACHE_EXPIRY, json.dumps(stock_data))
        return jsonify(stock_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Add stock purchase with company name fetching
@app.route("/add_stock", methods=["POST"])
def add_stock():
    data = request.json
    ticker, quantity, buy_price, currency, date = data["ticker"].upper(), data["quantity"], data["buy_price"], data["currency"], data["date"]
    
    try:
        datetime.strptime(date, "%d-%m-%Y")
        stock_info = fetch_stock_details(ticker).json
        company_name = stock_info.get("company_name", "Unknown")
        
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO positions (ticker, company_name, quantity, buy_price, currency, date) VALUES (?, ?, ?, ?, ?, ?)", 
                           (ticker, company_name, quantity, buy_price, currency, date))
            conn.commit()
        return jsonify({"message": "Stock position added successfully."})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Sell stock and calculate profit using FIFO
@app.route("/sell_stock", methods=["POST"])
def sell_stock():
    data = request.json
    ticker, sell_quantity, sell_price, sell_date = data["ticker"].upper(), abs(data["quantity"]), data["sell_price"], data["date"]
    
    try:
        datetime.strptime(sell_date, "%d-%m-%Y")
        total_profit = 0
        remaining_qty = sell_quantity
        
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, quantity, buy_price FROM positions WHERE ticker = ? ORDER BY date ASC", (ticker,))
            positions = cursor.fetchall()
            
            for position in positions:
                pos_id, qty, buy_price = position
                if remaining_qty == 0:
                    break
                
                if qty > remaining_qty:
                    profit = (sell_price - buy_price) * remaining_qty
                    total_profit += profit
                    cursor.execute("UPDATE positions SET quantity = quantity - ? WHERE id = ?", (remaining_qty, pos_id))
                    remaining_qty = 0
                else:
                    profit = (sell_price - buy_price) * qty
                    total_profit += profit
                    remaining_qty -= qty
                    cursor.execute("DELETE FROM positions WHERE id = ?", (pos_id,))
                
            cursor.execute("INSERT INTO transactions (ticker, quantity, sell_price, date, profit_loss) VALUES (?, ?, ?, ?, ?)", 
                           (ticker, -sell_quantity, sell_price, sell_date, total_profit))
            conn.commit()
        
        return jsonify({"message": "Stock sale recorded successfully.", "profit_loss": total_profit})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Check current stock positions
@app.route("/check_stocks", methods=["GET"])
def check_stocks():
    with sqlite3.connect(db_file) as conn:
        df = pd.read_sql_query("SELECT * FROM positions", conn)
    return df.to_json(orient="records")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
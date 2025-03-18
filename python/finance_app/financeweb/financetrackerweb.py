from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime
from collections import defaultdict

app = Flask(__name__)
db_file = "finance_tracker.db"

def init_db():
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                            id INTEGER PRIMARY KEY,
                            date TEXT NOT NULL,
                            type TEXT NOT NULL,
                            amount REAL NOT NULL,
                            category TEXT NOT NULL,
                            description TEXT)
                        ''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS savings (
                            id INTEGER PRIMARY KEY,
                            date TEXT NOT NULL,
                            amount REAL NOT NULL,
                            purpose TEXT NOT NULL)
                        ''')
        conn.commit()

@app.route("/add_transaction", methods=["POST"])
def add_transaction():
    data = request.json
    date, entry_type, amount, category, description = (
        data["date"], data["type"], data["amount"], data["category"], data["description"])
    
    try:
        datetime.strptime(date, "%d-%m-%Y")
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO transactions (date, type, amount, category, description) VALUES (?, ?, ?, ?, ?)", 
                           (date, entry_type, amount, category, description))
            conn.commit()
        return jsonify({"message": "Transaction added successfully."})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/get_transactions", methods=["GET"])
def get_transactions():
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transactions")
        transactions = cursor.fetchall()
    
    transactions_list = [
        {"id": row[0], "date": row[1], "type": row[2], "amount": row[3], "category": row[4], "description": row[5]} 
        for row in transactions
    ]
    return jsonify(transactions_list)

@app.route("/auto_savings", methods=["POST"])
def auto_savings():
    try:
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='Income'")
            total_income = cursor.fetchone()[0] or 0
            
            cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='Expense'")
            total_expense = cursor.fetchone()[0] or 0
            
            balance = total_income - total_expense
            if balance > 0:
                date_today = datetime.today().strftime('%d-%m-%Y')
                cursor.execute("INSERT INTO savings (date, amount, purpose) VALUES (?, ?, ?)", 
                               (date_today, balance, "End-of-month auto-savings"))
                conn.commit()
                return jsonify({"message": "Auto-savings added successfully", "amount_saved": balance})
            else:
                return jsonify({"message": "No surplus balance for savings."})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/monthly_summary", methods=["GET"])
def monthly_summary():
    try:
        monthly_data = defaultdict(lambda: {"income": 0, "expenses": 0, "savings": 0})
        total_savings = 0
        
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT date, type, amount FROM transactions")
            transactions = cursor.fetchall()
            
            for date, entry_type, amount in transactions:
                dt = datetime.strptime(date, "%d-%m-%Y")
                key = (dt.year, dt.month)
                if entry_type == "Income":
                    monthly_data[key]["income"] += amount
                elif entry_type == "Expense":
                    monthly_data[key]["expenses"] += amount
            
            cursor.execute("SELECT SUM(amount) FROM savings")
            total_savings = cursor.fetchone()[0] or 0
        
        summary_result = {
            f"{month:02d}-{year}": {
                "Income": values["income"],
                "Expenses": values["expenses"],
                "Balance": values["income"] - values["expenses"]
            } for (year, month), values in sorted(monthly_data.items())
        }
        summary_result["Total Savings"] = total_savings
        
        return jsonify(summary_result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    init_db()
    app.run(debug=True)

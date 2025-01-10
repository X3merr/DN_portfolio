import datetime

# Finance Tracker Application
class FinanceTracker:
    def __init__(self):
        self.data = {
            "income": [],
            "expenses": [],
            "investments": [],
            "savings": []
        }
    def add_income(self, amount, source, date):
        self.data["income"].append({
            "amount": amount,
            "source": source,
            "date": date
        })
        print(f"Income of {amount} from {source} added successfully!")
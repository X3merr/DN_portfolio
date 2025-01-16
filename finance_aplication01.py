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

    def add_expense(self, amount, category, date):
        self.data["expenses"].append({
            "amount": amount,
            "category": category,
            "date": date
        })
        print(f"Expense of {amount} for {category} added successfully!")

    def add_investment(self, amount, investment_type, date):
        self.data["investments"].append({
            "amount": amount,
            "type": investment_type,
            "date": date
        })
        print(f"Investment of {amount} in {investment_type} added successfully!")

    def add_savings(self, amount, purpose, date):
        self.data["savings"].append({
            "amount": amount,
            "purpose": purpose,
            "date": date
        })
        print(f"Savings of {amount} for {purpose} added successfully!")

        # Main function
def main():
    tracker = FinanceTracker()
    
    while True:
        print("\Finance Tracker Menu:")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. Add Investment")
        print("4. Add Savings")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            amount = float(input("Enter income amount: "))
            source = input("Enter income source: ")
            date = get_date_input()
            tracker.add_income(amount, source, date)
        elif choice == "2":
            amount = float(input("Enter expense amount: "))
            category = input("Enter expense category: ")
            date = get_date_input()
            tracker.add_expense(amount, category, date)
        elif choice == "3":
            amount = float(input("Enter investment amount: "))
            investment_type = input("Enter investment type: ")
            date = get_date_input()
            tracker.add_investment(amount, investment_type, date)
        elif choice == "4":
            amount = float(input("Enter savings amount: "))
            purpose = input("Enter savings purpose: ")
            date = get_date_input()
            tracker.add_savings(amount, purpose, date)
# Start application
if __name__ == "__main__":
    main()
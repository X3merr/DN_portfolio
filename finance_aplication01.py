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

    def view_summary(self):
        print("\n--- Finance Summary ---")
        for category, items in self.data.items():
            print(f"\n{category.capitalize()}:")
            for item in items:
                print(f"  Amount: {item['amount']}, "
                      f"Description: {item.get('source') or item.get('category') or item.get('type') or item.get('purpose')}, "
                      f"Date: {item['date'].strftime('%Y/%m/%d')}")
        print("\n--- End of Summary ---")

# Utility function to parse date input
def get_date_input():
    while True:
        date_input = input("Enter the date (YYYY/MM/DD) or press Enter for today: ")
        if not date_input.strip():
            return datetime.datetime.now()
        try:
            return datetime.datetime.strptime(date_input, "%Y/%m/%d")
        except ValueError:
            print("Invalid date format. Please use YYYY/MM/DD.")

# Main function
def main():
    tracker = FinanceTracker()
    
    while True:
        print("\Finance Tracker Menu:")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. Add Investment")
        print("4. Add Savings")
        print("5. View Summary")
        print("6. Exit")
        
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
        elif choice == "5":
            tracker.view_summary()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Start application
if __name__ == "__main__":
    main()
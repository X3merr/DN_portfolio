import datetime
from collections import defaultdict

# Finance Tracker Application
class FinanceTracker:
    def __init__(self):
        self.data = {
            "income": [],
            "expenses": [],
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

    def add_savings(self, amount, purpose, date):
        self.data["savings"].append({
            "amount": amount,
            "purpose": purpose,
            "date": date
        })
        print(f"Savings of {amount} for {purpose} added successfully!")

    def spend_savings(self, amount, purpose, date):
        """ Deduct a specific amount from savings while keeping track of purpose. """
        total_savings = sum(item["amount"] for item in self.data["savings"])
        
        if total_savings < amount:
            print("Not enough savings available to spend this amount.")
            return
        
        remaining_amount = amount
        updated_savings = []
        
        for item in self.data["savings"]:
            if remaining_amount > 0:
                if item["amount"] <= remaining_amount:
                    remaining_amount -= item["amount"]
                else:
                    item["amount"] -= remaining_amount
                    updated_savings.append(item)
                    remaining_amount = 0
            else:
                updated_savings.append(item)
        
        self.data["savings"] = updated_savings
        print(f"Savings spent: {amount} for {purpose} on {date.strftime('%d-%m-%Y')}.")

    def view_monthly_summary(self):
        monthly_data = defaultdict(lambda: {"income": 0, "expenses": 0, "savings": 0})
        total_savings = sum(item["amount"] for item in self.data["savings"])
        
        for entry in self.data["income"]:
            key = (entry["date"].year, entry["date"].month)
            monthly_data[key]["income"] += entry["amount"]
        
        for entry in self.data["expenses"]:
            key = (entry["date"].year, entry["date"].month)
            monthly_data[key]["expenses"] += entry["amount"]
        
        for entry in self.data["savings"]:
            key = (entry["date"].year, entry["date"].month)
            monthly_data[key]["savings"] += entry["amount"]
        
        print("\n--- Monthly Summary ---")
        for (year, month), values in sorted(monthly_data.items()):
            print(f"{month:02d}-{year} - Income: {values['income']}, Expenses: {values['expenses']}, Savings: {values['savings']}, Balance: {values['income'] - values['expenses']}")
        print(f"Total Savings (All time): {total_savings}")
        print("\n--- End of Monthly Summary ---")

# Utility function to parse date input
def get_date_input():
    while True:
        date_input = input("Enter the date (DD-MM-YYYY) or press Enter for today: ")
        if not date_input.strip():
            return datetime.datetime.now()
        try:
            return datetime.datetime.strptime(date_input, "%d-%m-%Y")
        except ValueError:
            print("Invalid date format. Please use DD-MM-YYYY.")

# Main function
def main():
    tracker = FinanceTracker()
    
    while True:
        print("\nFinance Tracker Menu:")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. Add Savings")
        print("4. Spend Savings")
        print("5. View Monthly Summary")
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
            amount = float(input("Enter savings amount: "))
            purpose = input("Enter savings purpose: ")
            date = get_date_input()
            tracker.add_savings(amount, purpose, date)
        elif choice == "4":
            amount = float(input("Enter amount to spend from savings: "))
            purpose = input("Enter spending purpose: ")
            date = get_date_input()
            tracker.spend_savings(amount, purpose, date)
        elif choice == "5":
            tracker.view_monthly_summary()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Start application
if __name__ == "__main__":
    main()

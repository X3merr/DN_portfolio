import datetime
import csv
import os
from collections import defaultdict

# Finance Tracker Application
class FinanceTracker:
    def __init__(self, csv_filename="overview.csv", inputs_csv="inputs.csv"):
        self.data = {
            "income": [],
            "expenses": [],
            "savings": []
        }
        self.csv_filename = csv_filename
        self.inputs_csv = inputs_csv
        self.initialize_csv(self.csv_filename)
        self.initialize_csv(self.inputs_csv)
        self.load_data_from_csv()
    
    def initialize_csv(self, filename):
        """Create the CSV file with headers if it does not exist."""
        try:
            with open(filename, "x", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Date", "Type", "Amount", "Category", "Description"])
        except FileExistsError:
            pass  # File already exists
    
    def load_data_from_csv(self):
        """Load existing data from CSV file into memory."""
        try:
            with open(self.csv_filename, "r") as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    date = datetime.datetime.strptime(row[0], '%d-%m-%Y')
                    entry_type, amount, category, description = row[1], float(row[2]), row[3], row[4]
                    if entry_type == "Income":
                        self.data["income"].append({"amount": amount, "source": description, "date": date})
                    elif entry_type == "Expense":
                        self.data["expenses"].append({"amount": amount, "category": category, "date": date})
                    elif entry_type == "Savings":
                        self.data["savings"].append({"amount": amount, "purpose": description, "date": date})
        except FileNotFoundError:
            pass
    
    def log_to_csv(self, filename, date, entry_type, amount, category, description):
        """Logs an entry to the specified CSV file."""
        with open(filename, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([date.strftime('%d-%m-%Y'), entry_type, amount, category, description])
    
    def log_to_inputs_csv(self, date, entry_type, amount, category, description):
        """Logs an entry to the inputs CSV file."""
        self.log_to_csv(self.inputs_csv, date, entry_type, amount, category, description)
    
    def add_income(self, amount, source, date):
        self.data["income"].append({
            "amount": amount,
            "source": source,
            "date": date
        })
        self.log_to_csv(self.csv_filename, date, "Income", amount, "Income", source)
        self.log_to_inputs_csv(date, "Income", amount, "Income", source)
        print(f"Income of {amount} from {source} added successfully!")
    
    def add_expense(self, amount, category, date):
        self.data["expenses"].append({
            "amount": amount,
            "category": category,
            "date": date
        })
        self.log_to_csv(self.csv_filename, date, "Expense", amount, category, "Expense logged")
        self.log_to_inputs_csv(date, "Expense", amount, category, "Expense logged")
        print(f"Expense of {amount} for {category} added successfully!")
    
    def add_savings(self, amount, purpose, date):
        self.data["savings"].append({
            "amount": amount,
            "purpose": purpose,
            "date": date
        })
        self.log_to_csv(self.csv_filename, date, "Savings", amount, "Savings", purpose)
        self.log_to_inputs_csv(date, "Savings", amount, "Savings", purpose)
        print(f"Savings of {amount} for {purpose} added successfully!")
    
    def get_last_day_of_month(self, year, month):
        """Returns the last day of the given month."""
        next_month = month % 12 + 1
        next_month_year = year if month < 12 else year + 1
        last_day = datetime.datetime(next_month_year, next_month, 1) - datetime.timedelta(days=1)
        return last_day.day
    
    def view_monthly_summary(self):
        monthly_data = defaultdict(lambda: {"income": 0, "expenses": 0, "savings": 0})
        total_savings = sum(item["amount"] for item in self.data["savings"])
        
        for entry in self.data["income"]:
            key = (entry["date"].year, entry["date"].month)
            monthly_data[key]["income"] += entry["amount"]
        
        for entry in self.data["expenses"]:
            key = (entry["date"].year, entry["date"].month)
            monthly_data[key]["expenses"] += entry["amount"]
        
        print("\n--- Monthly Summary ---")
        for (year, month), values in sorted(monthly_data.items()):
            balance = values['income'] - values['expenses']
            last_day = self.get_last_day_of_month(year, month)
            date = datetime.datetime(year, month, last_day)
            
            if balance > 0:  # Positive balance
                self.add_savings(balance, "End-of-month auto-savings", date)
            elif balance < 0 and total_savings >= abs(balance):  # Negative balance and sufficient savings
                adjustment = abs(balance)
                total_savings -= adjustment
                self.add_savings(-adjustment, "End-of-month debt adjustment", date)
            
            summary_line = f"{month:02d}-{year} - Income: {values['income']}, Expenses: {values['expenses']}, Balance: {balance}"
            print(summary_line)
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
        print("4. View Monthly Summary")
        print("5. Exit")
        
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
            tracker.view_monthly_summary()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

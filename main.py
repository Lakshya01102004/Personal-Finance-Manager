import os
os.makedirs("data", exist_ok=True)
print("Environment ready.")

class Expense:
    def __init__(self, amount, category, date, description):
        self.amount = float(amount)
        self.category = category
        self.date = date
        self.description = description

    def to_list(self):
        return [self.date, self.category, self.amount, self.description]

    def __str__(self):
        return f"{self.date} | {self.category} | ₹{self.amount} | {self.description}"


from datetime import datetime

def validate_amount(value):
    try:
        value = float(value)
        if value <= 0:
            raise ValueError
        return value
    except ValueError:
        print("Invalid amount. Enter a positive number.")
        return None


def validate_date(date_text):
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return date_text
    except ValueError:
        print("Date must be in YYYY-MM-DD format.")
        return None


def validate_non_empty(text, field):
    if not text.strip():
        print(f"{field} cannot be empty.")
        return None
    return text.strip()

import csv

EXPENSE_FILE = "data/expenses.csv"
BACKUP_FILE = "data/backup.csv"

def load_expenses():
    expenses = []
    try:
        with open(EXPENSE_FILE, "r") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                expenses.append(
                    Expense(row[2], row[1], row[0], row[3])
                )
    except FileNotFoundError:
        pass
    return expenses


def save_expenses(expenses):
    with open(EXPENSE_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Category", "Amount", "Description"])
        for exp in expenses:
            writer.writerow(exp.to_list())


def backup_data():
    if os.path.exists(EXPENSE_FILE):
        with open(EXPENSE_FILE, "r") as src, open(BACKUP_FILE, "w") as dest:
            dest.write(src.read())


from collections import defaultdict

def category_summary(expenses):
    summary = defaultdict(float)
    for exp in expenses:
        summary[exp.category] += exp.amount
    return summary


def total_expense(expenses):
    return sum(exp.amount for exp in expenses)


def average_expense(expenses):
    return total_expense(expenses) / len(expenses) if expenses else 0


def monthly_report(expenses, month):
    return [exp for exp in expenses if exp.date.startswith(month)]


def search_expenses(expenses, keyword):
    keyword = keyword.lower()
    return [
        exp for exp in expenses
        if keyword in exp.category.lower()
        or keyword in exp.description.lower()
        or keyword in exp.date
    ]


def show_menu():
    print("\n" + "=" * 45)
    print("        PERSONAL FINANCE MANAGER")
    print("=" * 45)
    print("1. Add New Expense")
    print("2. View All Expenses")
    print("3. Category-wise Summary")
    print("4. Monthly Report")
    print("5. Search Expenses")
    print("6. Backup Data")
    print("7. Exit")


def main():
    expenses = load_expenses()

    while True:
        show_menu()
        choice = input("Enter your choice (1-7): ")

        if choice == "1":
            amount = validate_amount(input("Enter amount: "))
            if amount is None: continue

            category = validate_non_empty(input("Enter category: "), "Category")
            if category is None: continue

            date = validate_date(input("Enter date (YYYY-MM-DD): "))
            if date is None: continue

            desc = validate_non_empty(input("Enter description: "), "Description")
            if desc is None: continue

            expenses.append(Expense(amount, category, date, desc))
            save_expenses(expenses)
            print("Expense added successfully.")

        elif choice == "2":
            if not expenses:
                print("No expenses recorded.")
            for exp in expenses:
                print(exp)

        elif choice == "3":
            summary = category_summary(expenses)
            for cat, amt in summary.items():
                print(f"{cat}: ₹{amt}")
            print("Total:", total_expense(expenses))
            print("Average:", round(average_expense(expenses), 2))

        elif choice == "4":
            month = input("Enter month (YYYY-MM): ")
            report = monthly_report(expenses, month)
            for r in report:
                print(r)
            print("Total:", total_expense(report))

        elif choice == "5":
            keyword = input("Enter search keyword: ")
            for r in search_expenses(expenses, keyword):1
        elif choice == "6":
            backup_data()
            print("Backup completed.")

        elif choice == "7":
            print("Exiting application.")
            break

        else:
            print("Invalid choice.")


main()



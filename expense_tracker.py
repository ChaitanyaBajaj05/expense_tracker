import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime

# Database setup
conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    description TEXT,
    date TEXT NOT NULL
)
""")
conn.commit()


# Functions
def add_expense(amount, category, description=""):
    date = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("INSERT INTO expenses (amount, category, description, date) VALUES (?, ?, ?, ?)",
                   (amount, category, description, date))
    conn.commit()


def view_expenses():
    cursor.execute("SELECT * FROM expenses")
    return cursor.fetchall()


def monthly_report(year, month):
    cursor.execute("SELECT category, SUM(amount) FROM expenses WHERE strftime('%Y', date)=? AND strftime('%m', date)=? GROUP BY category",
                   (str(year), f"{month:02}"))
    return cursor.fetchall()


def plot_expenses(year, month):
    data = monthly_report(year, month)
    if not data:
        print("No expenses for this month.")
        return

    categories = [d[0] for d in data]
    amounts = [d[1] for d in data]

    plt.figure(figsize=(6, 6))
    plt.pie(amounts, labels=categories, autopct="%1.1f%%", startangle=140)
    plt.title(f"Expenses for {year}-{month:02}")
    plt.show()


if __name__ == "__main__":
    while True:
        print("\nExpense Tracker Menu:")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Monthly Report")
        print("4. Plot Monthly Expenses")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            amt = float(input("Enter amount: "))
            cat = input("Enter category: ")
            desc = input("Enter description (optional): ")
            add_expense(amt, cat, desc)
            print("Expense added successfully!")

        elif choice == "2":
            expenses = view_expenses()
            for e in expenses:
                print(e)

        elif choice == "3":
            y = int(input("Enter year (YYYY): "))
            m = int(input("Enter month (MM): "))
            report = monthly_report(y, m)
            if report:
                for r in report:
                    print(r)
            else:
                print("No data found.")

        elif choice == "4":
            y = int(input("Enter year (YYYY): "))
            m = int(input("Enter month (MM): "))
            plot_expenses(y, m)

        elif choice == "5":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Try again.")

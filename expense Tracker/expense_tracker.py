# Personal Finance Tracker 
# Author: Shivani Narayan
# Mini  project B.Tech for second year

# ----- Load old data or create new files -----
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
try:
    expenses = pd.read_excel("expenses.xlsx")
except:
    expenses = pd.DataFrame(columns=["Date", "Description", "Amount", "Category", "Payment Method"])

try:
    income = pd.read_excel("income.xlsx")
except:
    income = pd.DataFrame(columns=["Date", "Source", "Amount", "Payment Method"])

# ----- MAIN MENU -----
while True:
    print("\n--- My Personal Finance Menu ---")
    print("1. Expense Manager")
    print("2. Income Manager")
    print("3. Reports & Savings")
    print("4. Exit")

    choice = input("Choose option (1-4): ")

    # ================= EXPENSE MANAGER =================
    if choice == "1":
        print("\n--- Expense Manager ---")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Monthly Summary")
        print("4. Yearly Summary")
        print("5. Search by Keyword")
        print("6. Filter by Category")
        print("7. Edit Expense")
        print("8. Delete Expense")
        print("9. Show Chart")
        print("10. Back")

        ch = input("Choose option (1-10): ")

        if ch == "1":
            date = input("Date (dd-mm-yyyy): ")
            desc = input("Description: ")
            try:
                amt = float(input("Amount: "))
            except:
                print("Invalid amount!")
                continue
            cat = input("Category: ")
            pay = input("Payment Method: ")

            new_exp = pd.DataFrame([[date, desc, amt, cat, pay]],
                                   columns=["Date", "Description", "Amount", "Category", "Payment Method"])
            expenses = pd.concat([expenses, new_exp], ignore_index=True)
            expenses.to_excel("expenses.xlsx", index=False)
            print("Expense Added!")

        elif ch == "2":
            print(expenses if not expenses.empty else "No expenses yet.")

        elif ch == "3":
            expenses["Date"] = pd.to_datetime(expenses["Date"], errors="coerce")
            m = int(input("Enter month (1-12): "))
            y = int(input("Enter year: "))
            mdata = expenses[(expenses["Date"].dt.month == m) & (expenses["Date"].dt.year == y)]
            print(mdata if not mdata.empty else "No records found.")

        elif ch == "4":
            expenses["Date"] = pd.to_datetime(expenses["Date"], errors="coerce")
            y = int(input("Enter year: "))
            ydata = expenses[expenses["Date"].dt.year == y]
            print(ydata if not ydata.empty else "No records found.")

        elif ch == "5":
            word = input("Enter keyword: ").lower()
            res = expenses[expenses["Description"].str.lower().str.contains(word, na=False)]
            print(res if not res.empty else "No match found.")

        elif ch == "6":
            cat = input("Enter Category: ").lower()
            res = expenses[expenses["Category"].str.lower() == cat]
            print(res if not res.empty else "No match found.")

        elif ch == "7":
            print(expenses)
            i = int(input("Row number to edit: "))
            if i < 0 or i >= len(expenses):
                print("Invalid index.")
                continue
            new_amt = input(f"New Amount ({expenses.at[i,'Amount']}): ")
            if new_amt.strip():
                expenses.at[i, "Amount"] = float(new_amt)
            expenses.to_excel("expenses.xlsx", index=False)
            print("Updated!")

        elif ch == "8":
            print(expenses)
            i = int(input("Row number to delete: "))
            expenses = expenses.drop(i).reset_index(drop=True)
            expenses.to_excel("expenses.xlsx", index=False)
            print("Deleted!")

        elif ch == "9":
            if expenses.empty:
                print("No data for chart.")
            else:
                group = expenses.groupby("Category")["Amount"].sum()
                group.plot(kind="bar", title="Expenses by Category")
                plt.show()

        elif ch == "10":
            continue

    # ================= INCOME MANAGER =================
    elif choice == "2":
        print("\n--- Income Manager ---")
        print("1. Add Income")
        print("2. View All Income")
        print("3. Edit Income")
        print("4. Delete Income")
        print("5. Back")

        ch = input("Choose option (1-5): ")

        if ch == "1":
            date = input("Date (dd-mm-yyyy): ")
            src = input("Source (salary, gift, etc.): ")
            try:
                amt = float(input("Amount: "))
            except:
                print("Invalid amount!")
                continue
            pay = input("Payment Method: ")

            new_inc = pd.DataFrame([[date, src, amt, pay]],
                                   columns=["Date", "Source", "Amount", "Payment Method"])
            income = pd.concat([income, new_inc], ignore_index=True)
            income.to_excel("income.xlsx", index=False)
            print("Income Added!")

        elif ch == "2":
            try:
                income = pd.read_excel("income.xlsx")   # reload
            except:
                income = pd.DataFrame(columns=["Date","Source","Amount","Payment Method"])
            print(income if not income.empty else "No income records.")

        elif ch == "3":
            print(income)
            i = int(input("Row number to edit: "))
            new_amt = input(f"New Amount ({income.at[i,'Amount']}): ")
            if new_amt.strip():
                income.at[i,"Amount"] = float(new_amt)
            income.to_excel("income.xlsx", index=False)
            print("Updated!")

        elif ch == "4":
            print(income)
            i = int(input("Row number to delete: "))
            income = income.drop(i).reset_index(drop=True)
            income.to_excel("income.xlsx", index=False)
            print("Deleted!")

        elif ch == "5":
            continue

    # ================= REPORTS =================
    elif choice == "3":
        print("\n--- Reports & Savings ---")
        total_exp = expenses["Amount"].sum()
        total_inc = income["Amount"].sum()
        balance = total_inc - total_exp

        print(f"Total Income: {total_inc}")
        print(f"Total Expenses: {total_exp}")
        print(f"Savings (Balance): {balance}")

        # Budget checking
        try:
            budget = float(input("Enter your monthly budget: "))
            if total_exp > budget:
                print(f"⚠ Over budget by {total_exp - budget}")
            else:
                print(f"✅ Under budget by {budget - total_exp}")
        except:
            print("No budget entered.")

    # ================= EXIT =================
    elif choice == "4":
        print("Bye! Data saved.")

    break   # exit loop properly


import os
import time

expenses = []          # each item: (date, description, category, amount)

# Always save/load in this exact folder, no matter where the program is run from.
FOLDER = r"C:\Python Starting\Projects"
FILENAME = os.path.join(FOLDER, "expenses.txt")


# ------------------------------------------------------------- small helpers
def ask_text(message):
    """Keeps asking until the answer isn't empty, then returns it."""
    while True:
        value = input(message).strip()
        if value == "":
            print(" This cannot be empty! ")
        elif " | " in value:
            print(" Please do not use ' | ' in your answer. ")
        else:
            return value


def ask_amount(message):
    """Keeps asking until the answer is a whole number above 0."""
    while True:
        try:
            amount = int(input(message).strip())
        except ValueError:
            print(" Enter Only Integer Value! ")
            continue
        if amount <= 0:
            print(f" Amount cannot be {amount}, it must be above 0 ")
            continue
        return amount


def ask_yes_no(message):
    """Keeps asking until the answer is exactly 'yes' or 'no'."""
    while True:
        answer = input(message).strip().lower()
        if answer in ("yes", "no"):
            return answer
        print(" Enter yes or no only ")


def find_by_date(date):
    """Returns the position of the first expense with this date, or -1."""
    for i, expense in enumerate(expenses):
        if expense[0] == date:
            return i
    return -1


# ------------------------------------------------------------------- saving
def save_data():
    """Writes expenses.txt safely: build the new file in full, then swap it
    in. If anything goes wrong mid-write, the old file is untouched."""
    os.makedirs(FOLDER, exist_ok=True)   # creates the folder if it's missing
    temp_name = FILENAME + ".tmp"

    w_date = max([len("Date")] + [len(e[0]) for e in expenses])
    w_desc = max([len("Description")] + [len(e[1]) for e in expenses])
    w_cat = max([len("Category")] + [len(e[2]) for e in expenses])
    w_amt = max([len("Amount")] + [len(str(e[3])) for e in expenses])
    line = "=" * (w_date + w_desc + w_cat + w_amt + 9)

    with open(temp_name, "w") as file:
        file.write(line + "\n")
        file.write(f"{'Date':<{w_date}} | {'Description':<{w_desc}} | "
                   f"{'Category':<{w_cat}} | {'Amount':<{w_amt}}\n")
        file.write(line + "\n")
        for e in expenses:
            file.write(f"{e[0]:<{w_date}} | {e[1]:<{w_desc}} | "
                       f"{e[2]:<{w_cat}} | {str(e[3]):<{w_amt}}\n")
        file.write(line + "\n")

    os.replace(temp_name, FILENAME)    # only swapped in once the write succeeded


def load_data():
    """Reads expenses.txt. Skips any line it can't understand instead of
    crashing the whole program."""
    try:
        with open(FILENAME, "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        return

    for line in lines[3:-1]:
        if line.strip() == "":
            continue
        try:
            parts = line.split(" | ")
            date = parts[0].strip()
            description = parts[1].strip()
            category = parts[2].strip()
            amount = int(parts[3].strip())
            expenses.append((date, description, category, amount))
        except (IndexError, ValueError):
            print(f" Skipped a line that could not be read: {line.strip()} ")


# --------------------------------------------------------------------- CRUD
def add_expense():
    while True:
        date = ask_text(" Enter Date: ").lower()
        description = ask_text(" Enter Description: ")
        category = ask_text(" Enter Category: ").lower()
        amount = ask_amount(" Enter Amount: ")

        expenses.append((date, description, category, amount))
        save_data()
        print(" Expense added. ")

        if ask_yes_no(" Add another expense? (yes/no): ") == "no":
            return


def view_expenses():
    if len(expenses) == 0:
        print(" No Expenses Made ".center(50))
        return
    print("All Expenses:")
    for number, expense in enumerate(expenses, start=1):
        print(f"{number}. Date: {expense[0]}")
        print(f"   Description: {expense[1]}")
        print(f"   Category: {expense[2]}")
        print(f"   Amount: {expense[3]}")
        print()


def search_expenses():
    if len(expenses) == 0:
        print(" Expenses List is Empty! ")
        return

    def show(expense):
        print(f"\nDate: {expense[0]}\nDescription: {expense[1]}"
             f"\nCategory: {expense[2]}\nAmount: {expense[3]}\n")

    date = ask_text(" Enter Date of Expense: ").lower()
    found = False
    for expense in expenses:
        if expense[0] == date:
            show(expense)
            found = True
    if found:
        return

    category = ask_text(" Date not found. Enter Category: ").lower()
    for expense in expenses:
        if expense[2] == category:
            show(expense)
            found = True
    if found:
        return

    amount = ask_amount(" Not found. Enter Amount: ")
    for expense in expenses:
        if expense[3] == amount:
            show(expense)
            found = True
    if not found:
        print(" No expense Found ".center(40))


def update_expense():
    if len(expenses) == 0:
        print(" Expenses List is Empty! ")
        return

    view_expenses()
    while True:
        date = ask_text(" Enter the Date of the expense to Update: ").lower()
        position = find_by_date(date)
        if position != -1:
            break
        print(f" No expense of '{date}' date ")
        if ask_yes_no(" Try another date? (yes/no): ") == "no":
            return

    expense = expenses[position]
    while True:
        field = input(" What do you want to update? "
                      "(date / description / category / amount): ").strip().lower()
        match field:
            case "date":
                new_value = ask_text(" Enter new date: ").lower()
                expenses[position] = (new_value, expense[1], expense[2], expense[3])
            case "description":
                new_value = ask_text(" Enter new description: ")
                expenses[position] = (expense[0], new_value, expense[2], expense[3])
            case "category":
                new_value = ask_text(" Enter new category: ").lower()
                expenses[position] = (expense[0], expense[1], new_value, expense[3])
            case "amount":
                new_value = ask_amount(" Enter new amount: ")
                expenses[position] = (expense[0], expense[1], expense[2], new_value)
            case "":
                print(" Input cannot be empty ")
                continue
            case _:
                print(" Enter date, description, category or amount only ")
                continue

        save_data()
        print(f" Updated successfully to '{new_value}' ")
        return


def delete_expense():
    if len(expenses) == 0:
        print(" Expenses List is Empty! ")
        return

    view_expenses()
    while True:
        date = ask_text(" Enter date of expense to delete: ").lower()
        position = find_by_date(date)
        if position != -1:
            break
        print(" Date not found. ")
        if ask_yes_no(" Try another date? (yes/no): ") == "no":
            return

    expense = expenses[position]
    print(f"\nDate: {expense[0]}\nDescription: {expense[1]}"
         f"\nCategory: {expense[2]}\nAmount: {expense[3]}\n")

    if ask_yes_no(" Confirm delete? (yes/no): ") == "yes":
        expenses.pop(position)
        save_data()
        print(f" '{date}' expense deleted successfully. ")
    else:
        print(" Cancelled, nothing was deleted. ")


def clear_all():
    if len(expenses) == 0:
        print(" Nothing to clear. ")
        return
    if ask_yes_no(f" Delete ALL {len(expenses)} expenses? This cannot be undone. (yes/no): ") == "yes":
        expenses.clear()
        save_data()
        print(" All expenses cleared successfully. ")
    else:
        print(" Cancelled, nothing was cleared. ")


def show_statistics():
    if len(expenses) == 0:
        print(" Expenses list is empty. ")
        return

    amounts = [e[3] for e in expenses]
    total = sum(amounts)
    average = total / len(expenses)
    highest = max(expenses, key=lambda e: e[3])
    lowest = min(expenses, key=lambda e: e[3])

    per_category = {}
    for e in expenses:
        per_category[e[2]] = per_category.get(e[2], 0) + e[3]

    print(f"Total number of expenses: {len(expenses)}")
    print(f"Total money spent: {total}")
    print(f"Average expense: {average:.2f}")
    print(f"Highest expense: {highest[1]} ({highest[0]}) - {highest[3]}")
    print(f"Lowest expense: {lowest[1]} ({lowest[0]}) - {lowest[3]}")
    print("Spending by category:")
    for category, spent in sorted(per_category.items(), key=lambda row: row[1], reverse=True):
        print(f"  {category}: {spent}")


def exit_all():
    save_data()
    print(" Program Close Success ".center(50))
    print("=" * 36)
    time.sleep(1.5)
    raise SystemExit


# ---------------------------------------------------------------------- menu
def menu():
    while True:
        print("\n" + "=" * 40)
        print("          EXPENSE TRACKER")
        print("=" * 40)
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Search Expenses")
        print("4. Update Expense")
        print("5. Delete Expense")
        print("6. Show Statistics")
        print("7. Clear All Expenses")
        print("8. Exit")
        print("=" * 40)

        choice = input("Enter your choice: ").strip().lower()
        print()

        match choice:
            case "1":
                add_expense()
            case "2":
                view_expenses()
            case "3":
                search_expenses()
            case "4":
                update_expense()
            case "5":
                delete_expense()
            case "6":
                show_statistics()
            case "7":
                clear_all()
            case "8":
                exit_all()
            case "":
                print(" Input cannot be empty ")
            case _:
                print(" Invalid Input. Enter only digits, e.g. 1, 2 ")


if __name__ == "__main__":
    load_data()
    menu()
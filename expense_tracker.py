import csv
import os

class InvalidAmountError(Exception):
    #Raised when expense amouny is zero or negative.
    pass

class Expense:
    #Base class representing a single expense entry
    def __init__(self, expense_id, date, category, description, amount):
        self.expense_id = expense_id
        self.date = date
        self.category = category
        self.description = description

        if float(amount) <= 0:
            raise InvalidAmountError("Amount must be poritive.")
        self.amount = float(amount)

    def to_dict(self):
        return {
            "expense_id": self.expense_id,
            "date": self.date,
            "category": self.category,
            "description": self.description,
            "amount": self.amount
        }

class ExpenseManager(Expense):
    '''Derived class that handle file I/O and CRUD operations.'''
    FIELDNAMES = ["expense_id","date", "category", "description", "amount"]

    def __init__(self, filename="expenses.csv"):
        self.filename = filename
        if not os.path.exists(self.filename):
            self._create_file()

    def _create_file(self):
        with open(self.filename, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.FIELDNAMES)
            writer.writeheader()

    def load_expenses(self):
        try:
            with open(self.filename, "r", newline="") as f:
                reader = csv.DictReader(f)
                return [row for row in reader]
        except FileNotFoundError:
            self._create_file()
            return[]
        
    def get_next_id(self):
        records = self.load_expenses()
        if not records:
            return 1
        return max(int(r["expense_id"]) for r in records) + 1
    
    def add_expense(self, date, category, desciption, amount):
        expense_id = self.get_next_id()
        new_expense = Expense(expense_id, date, category, desciption, amount)

        with open(self.filename, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.FIELDNAMES)
            writer.writerow(new_expense.to_dict())

        print(f"Expense added successfully with expense ID {expense_id}.")

    def view_expenses(self):
        records = self.load_expenses()
        if not records:
            print("No records found")
            return
        
        print(f"{'ID':<5}{'Date':<12}{'Category':<12}{'Description':<20}{'Amount':<10}")
        for r in records:
            print(f"{r['expense_id']:<5}{r['date']:<12}{r['category']:<12}{r['description']:<20}{r['amount']:<10}")

    def search_by_category(self, category):
        records = self.load_expenses()
        matches = [r for r in records if r["category"].lower() == category.lower()]

        if not matches:
            print(f"No expenses found for category '{category}'.")
            return
        
        for r in matches:
            print(f"{r['expense_id']:<5}{r['date']:<12}{r['category']:<12}{r['description']:<20}{r['amount']:<10}")

    def update_expense(self, expense_id, new_amount=None, new_description=None):
        records=self.load_expenses()
        found = False

        for r in records:
            if r["expense_id"] == str(expense_id):
                found = True
                if new_amount is not None:
                    if float(new_amount) <= 0:
                        raise InvalidAmountError("Amount must be positive.")
                    r["amount"] = float(new_amount)
                if new_description is not None:
                    r["description"] = new_description

        if not found:
            print("Record not found.")
            return
            
        self._rewrite_file(records)
        print(f"Expense ID {expense_id} updates successfully.")

    def delete_expense(self, expense_id):
        records = self.load_expenses()
        filtered = [r for r in records if r["expense_id"] != str(expense_id)]

        if len(filtered) == len(records):
            print("Record not found.")
            return
        
        self._rewrite_file(filtered)
        print(f"Expense ID {expense_id} deleted successfully.")

    def _rewrite_file(self, records):
        with open(self.filename, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.FIELDNAMES)
            writer.writeheader()
            writer.writerows(records)

    def monthly_summary(self, month):
        records = self.load_expenses()
        summary = {}

        for r in records:
            if ["date"][3:5] == month:
                category = r["category"]
                summary[category] = summary.get(category, 0) + float(r["amount"])

        if not summary:
            print(f"No expenses found for the month {month}.")
            return

        print(f"Monthly Summary for {month}: ") 
        for category, total in summary.items():
            print(f"{category}: {total:.2f}") 

def main_menu():
    manager = ExpenseManager()

    while True:
        print("\n       Personal Expense Tracker        ")
        print("1. Add new expense")
        print("2. View all expenses")
        print("3. Search by category")
        print("4. Update Expense")
        print("5. Delete Expense")
        print("6. View Monthly Summary")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ")

        try:
            if choice == "1":
                date = input("Enter date (DD-MM-YYYY): ")
                category = input("Enter category: ")
                description = input("Enter description: ")
                amount = input("Enter amount: ")
                manager.add_expense(date, category, description, amount)

            elif choice == "2":
                manager.view_expenses()

            elif choice == "3":
                category = input("Enter category to search: ")
                manager.search_by_category(category)

            elif choice == "4":
                expense_id = input("Enter expense ID to update: ")
                new_amount = input("Enter new amount (leave blank to skip): ")
                new_description = input("Enter new description (leave blank to skip): ")
                manager.update_expense(
                    expense_id,
                    new_amount if new_amount else None,
                    new_description if new_description else None,
                )

            elif choice == "5":
                expense_id = input("Enter expense_id to delete: ")
                manager.delete_expense(expense_id)

            elif choice == "6":
                month = input('Enter month (MM): ')
                manager.monthly_summary(month)

            elif choice == "7":
                print("Saving and exiting. Goodbye!")
                break

            else:
                print("Invalid choice. Please enter a number between 1 amd 7.")

        except InvalidAmountError as e:
                print(f"Error: {e}")
        except ValueError:
            print("Error: Please enter a valid numeric value.")
        except (IndexError, KeyError):
            print("Error: Record not found.")
        except PermissionError:
            print("Error: File is locked by another process. Try again later.")

if __name__ == "__main__":
    main_menu()
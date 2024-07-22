import json


class ExpenseSharingApp:
    def __init__(self):
        self.users = {}
        self.expenses = []

    def add_user(self, name):
        if name in self.users:
            print(f"User {name} already exists.")
        else:
            self.users[name] = 0
            print(f"User {name} added.")

    def add_expense(self, description, amount, split_type='equal', custom_shares=None):
        if split_type == 'equal':
            share = amount / len(self.users)
            for user in self.users:
                self.users[user] -= share
            self.expenses.append({
                'description': description,
                'amount': amount,
                'split_type': 'equal',
                'custom_shares': {}
            })
        elif split_type == 'custom':
            if custom_shares and sum(custom_shares.values()) == amount:
                for user, share in custom_shares.items():
                    if user in self.users:
                        self.users[user] -= share
                    else:
                        print(f"User {user} not found.")
                self.expenses.append({
                    'description': description,
                    'amount': amount,
                    'split_type': 'custom',
                    'custom_shares': custom_shares
                })
            else:
                print("Custom shares do not match the total amount or some users are missing.")
        else:
            print("Invalid split type.")

    def show_balances(self):
        print("\nCurrent Balances:")
        for user, balance in self.users.items():
            print(f"{user}: ${balance:.2f}")

    def show_summary(self):
        print("\nExpense Summary:")
        for expense in self.expenses:
            description = expense['description']
            amount = expense['amount']
            split_type = expense['split_type']
            print(f"{description}: rupees{amount:.2f} split {split_type}")
            if split_type == 'custom':
                for user, share in expense['custom_shares'].items():
                    print(f"  {user} paid rupees1{share:.2f}")

    def save_data(self, filename):
        data = {
            'users': self.users,
            'expenses': self.expenses
        }
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Data saved to {filename}.")

    def load_data(self, filename):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                self.users = data['users']
                self.expenses = data['expenses']
            print(f"Data loaded from {filename}.")
        except FileNotFoundError:
            print("File not found. Starting with an empty app.")
        except json.JSONDecodeError:
            print("Error decoding JSON. Starting with an empty app.")


def main():
    app = ExpenseSharingApp()

    while True:
        print("\nOptions:")
        print("1. Add User")
        print("2. Add Expense")
        print("3. Show Balances")
        print("4. Show Summary")
        print("5. Save Data")
        print("6. Load Data")
        print("7. Exit")

        choice = input("Enter choice: ")

        if choice == '1':
            name = input("Enter user name: ")
            app.add_user(name)
        elif choice == '2':
            description = input("Enter expense description: ")
            amount = float(input("Enter expense amount: "))
            split_type = input("Enter split type (equal/custom): ").strip().lower()
            custom_shares = {}
            if split_type == 'custom':
                for user in app.users:
                    share = float(input(f"Enter amount for {user}: "))
                    custom_shares[user] = share
            app.add_expense(description, amount, split_type, custom_shares)
        elif choice == '3':
            app.show_balances()
        elif choice == '4':
            app.show_summary()
        elif choice == '5':
            filename = input("Enter filename to save data: ")
            app.save_data(filename)
        elif choice == '6':
            filename = input("Enter filename to load data: ")
            app.load_data(filename)
        elif choice == '7':
            print("Exiting the app.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()

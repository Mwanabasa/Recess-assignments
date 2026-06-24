# Parent Class
class Transaction:
    def __init__(self, amount=0):
        self.amount = amount

    # Simulated method overloading using default parameters
    def process(self, account_balance, fee=0):
        """Base process method (to be overridden)."""
        return account_balance


# Child Class: Deposit
class Deposit(Transaction):
    def process(self, account_balance, fee=0):
        """Override: deposit increases balance."""
        print(f"Depositing {self.amount}...")
        return account_balance + self.amount


# Child Class: Withdrawal
class Withdrawal(Transaction):
    def process(self, account_balance, fee=0):
        """Override: withdrawal decreases balance."""
        print(f"Withdrawing {self.amount}...")
        total = self.amount + fee
        if total > account_balance:
            print("❌ Insufficient funds")
            return account_balance
        return account_balance - total


# Child Class: Transfer
class Transfer(Transaction):
    def process(self, account_balance, fee=0):
        """Override: transfer deducts from one account."""
        print(f"Transferring {self.amount}...")
        total = self.amount + fee
        if total > account_balance:
            print("❌ Transfer failed: insufficient funds")
            return account_balance
        return account_balance - total


# Demonstration
balance = 1000
print(f"Initial Balance: {balance}\n")

# Employer deposits salary
deposit = Deposit(500)
balance = deposit.process(balance)
print(f"Balance after deposit: {balance}\n")

# Employee withdraws money
withdraw = Withdrawal(200)
balance = withdraw.process(balance, fee=5)  # method overloading via optional fee
print(f"Balance after withdrawal: {balance}\n")

# Employee transfers funds
transfer = Transfer(300)
balance = transfer.process(balance, fee=10)
print(f"Balance after transfer: {balance}\n")

print("Final Account Balance:", balance)
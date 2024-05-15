# holdes teh calculations for testing file

def add(num1: int, num2: 2):
    return num1 + num2

def substract(num1: int, num2: int):
    return num1 - num2

def multiply(num1: int, num2: int):
    return num1 * num2

def devide(num1: int, num2: int):
    return num1 / num2

# creating our own exception class
class InsufficientFunds(Exception):
    pass


# testing a class:
class BankAccount():
    def __init__(self, starting_balance=0):  # if no balance is given then = 0
        self.balance = starting_balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientFunds("Insufficient funds in account")
        self.balance -= amount

    def collect_interest(self):
        self.balance *= 1.1

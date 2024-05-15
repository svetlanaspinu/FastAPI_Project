# this file will test a part of our code
# a test is just a function or method
import pytest # pentru a insera decoratorul @ - above the function
from app.calculations import add, substract, multiply, devide, BankAccount, InsufficientFunds #importing the function from the file calculations.py

# fixture(iys a function) este un tool al pytestului that helps us to minimize the amount of repetitve code. it runs before a testcase
# fixture is good to be used when working with database, inserting emails taht is manually
@pytest.fixture
#creating a name for the fixture
def zero_bank_account():
# return an initial of BankAccount with the initial of zero
    return BankAccount()

@pytest.fixture
def bank_account():
# return a given value=50
    return BankAccount(50)

# _add este functia din file-ul calculations.py
# folosim functia din decoarator- @ ca sa nu introducem fiecare nr aparte dar sa fie automat assigned datorita parametrize.
@pytest.mark.parametrize("num1, num2, expected", [
    (3, 2, 5),    # in lista sprimul nukar este num1 urmeaza num2 si rezultatul-expected.
    (7, 1, 8),
    (12, 4, 16)
])
def test_add(num1, num2, expected):
    print("testing add function")
# the assert statement is a powerful debugging tool that helps you validate assumptions about your code.
# if is true nothig is gonna happend its gonna print what is in the print statement; if False- error.
    assert add (num1, num2) == expected

def test_substract():
    assert substract(9, 4) == 5

def test_multiply():
    assert multiply(9, 4) == 36

def test_devide():
    assert devide(25, 5) == 5

# in paranreza calling the bank_account fixture
def test_bank_set_initial_amount(bank_account):
# removing this after fixture
    #bank_account = BankAccount(50)
    assert bank_account.balance == 50
    
# test for Bank account/ calling the fixture function(din paranteza), before to run the taste case, after whatever it returns in @pytest.fixture- def bank_account
# get passed into the variable - zero_bank_account, instead crrated an BankACCOUNT WE CAN JUST CALL THE zero_bank_account
def test_bank_default_amount(zero_bank_account):
    #bank_account = BankAccount()
    #assert bank_account.balance == 0
    assert zero_bank_account.balance == 0

def test_withdraw(bank_account):
    #bank_account = BankAccount(50) removed after calling the fixture
    bank_account.withdraw(20)
    assert bank_account.balance == 30

def test_deposit(bank_account):
    #bank_account = BankAccount(50) removed after calling the fixture
    bank_account.deposit(30)
    assert bank_account.balance == 80

def test_collect_interest(bank_account):
    #bank_account = BankAccount(50)
    bank_account.collect_interest()
# la aceasta functie avem erroare pt ca e outputul e nr cu sutime ex - 0.9999, folosim round method si nr.6 ca sa aduca aproape de 6- deoarece e 55. ca sa ne faca nr intreg
    assert round(bank_account.balance, 6)  == 55

# using fixed and parametrize to test multiple functuons
@pytest.mark.parametrize("deposited, withdrew, expected", [
    (200, 100, 100),    # in lista sprimul nukar este num1 urmeaza num2 si rezultatul-expected.
    (50, 10, 40),
    (1200, 200, 1000)
    
])

def test_bank_transaction(zero_bank_account, deposited, withdrew, expected): # zero_bank_account starting wirh zero as in function calculations file
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected

# everytime we through an error it will make the test fail/ for tha we have to create a diffrent test case
# using the zero bankk account from fixed
def test_insufficient_funds(bank_account):# in paranteze we haveb no money in account
    # tell python that we expect an error/exception and will consider the test is passing. if the bank_account.withdraw(200) will be an error pytho will expected and accepted
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(200)

  


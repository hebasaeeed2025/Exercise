import pytest
import datetime
from bank_account import BankAccount

@pytest.fixture
def bank_account():
    return BankAccount("Alice", 1000)

#Account Creation Tests
#1. Create an account with a valid initial balance
def test_create_account_valid(bank_account):
    assert bank_account.balance == 1000
    assert bank_account.account_holder == "Alice"

#2. Attempt to create an account with a negative balance (should raise ValueError)
def test_create_account_invalid():
    with pytest.raises(ValueError, match="Initial balance cannot be negative"):
        BankAccount("Alice", -1000)
    
#3. Ensure the account holder's name is stored correctly
def test_account_holder_name_stored_correctly(bank_account):
    assert bank_account.account_holder == "Alice"


#Deposit Tests
#1. Deposit a valid amount successfully
def test_deposit_valid_amount_successfully(bank_account):
    new_balance = bank_account.deposit(500)
    assert new_balance == 1500

#2. Attempt to deposit zero (should raise ValueError)
def test_deposit_zero(bank_account):
    with pytest.raises(ValueError, match="Deposit amount must be positive"):
        bank_account.deposit(0)

#3. Attempt to deposit a negative amount (should raise ValueError)
def test_deposit_negative(bank_account):
    with pytest.raises(ValueError, match="Deposit amount must be positive"):
        bank_account.deposit(-500)

#Withdrawal Tests
#1. Withdraw an amount successfully
def test_withdraw_valid_amount(bank_account):
    new_balance = bank_account.withdraw(500)
    assert new_balance == 500


#2. Attempt to withdraw more than available balance (should raise ValueError)
def test_withdraw_exceed_balance():
    account = BankAccount("Alice", 500)
    with pytest.raises(ValueError, match="Insufficient funds"):
        account.withdraw(600)

#3. Attempt to withdraw zero or negative amount (should raise ValueError)
def test_withdraw_invalid_amount(bank_account):
    with pytest.raises(ValueError, match="Withdrawal amount must be positive"):
        bank_account.withdraw(0)
    with pytest.raises(ValueError, match="Withdrawal amount must be positive"):
        bank_account.withdraw(-100)


#Transfer Tests
#1.Transfer an amount successfully
def test_transfer_amount_valid():
    sender = BankAccount("Alice", 1000)
    recipient = BankAccount("Bob", 500)
    sender.transfer(recipient, 300)
    assert sender.balance == 700
    assert recipient.balance == 800

#2. Attempt to transfer more than available balance (should raise ValueError)
def test_transfer_exceed_balance():
    sender = BankAccount("Alice", 500)
    recipient = BankAccount("Bob", 500)
    with pytest.raises(ValueError, match="Insufficient funds"):
        sender.transfer(recipient, 600)


#3. Attempt to transfer to a non-BankAccount object (should raise TypeError)
def test_transfer_invalid_recipient():
    sender = BankAccount("Alice", 1000)
    with pytest.raises(TypeError, match="Recipient must be a BankAccount instance"):
        sender.transfer("NotABankAccount", 100)


#Transaction History Tests
#1. Ensure transactions are recorded correctly
def test_transaction_recording(bank_account):
    bank_account.deposit(200)
    bank_account.withdraw(100)
    history = bank_account.get_transaction_history()
    assert len(history) == 3  
    

#2. Verify transaction history contains correct details
def test_transaction_details(bank_account):
    bank_account.deposit(200)
    last_transaction = bank_account.get_transaction_history()[-1]
    assert last_transaction["type"] == "Deposit"
    assert last_transaction["amount"] == 200
    assert last_transaction["balance_after"] == 1200


#3. Ensure transaction timestamps are present
def test_transaction_timestamp(bank_account):
    bank_account.deposit(200)
    last_transaction = bank_account.get_transaction_history()[-1]
    assert "timestamp" in last_transaction
    assert isinstance(last_transaction["timestamp"], datetime.datetime)



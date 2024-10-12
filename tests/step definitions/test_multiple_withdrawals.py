from pytest_bdd import scenarios, given, when, then, parsers

# Load the feature file
scenarios('../features/multiple_withdrawals.feature')

# Define a dictionary to simulate account balance
account = {}

@given(parsers.parse('I have an account with $"{balance:d}" balance'))
def setup_account(balance, logger):
    account['balance'] = int(balance)
    logger.info('I have an account with '+str(balance)+' balance')

@when(parsers.parse('I withdraw $"{amount:d}"'))
def withdraw(amount):
    amount = int(amount)
    # Check if the account has sufficient funds before withdrawing
    if account['balance'] >= amount:
        account['balance'] -= amount
    else:
        account['balance'] = 'Declined'

@then(parsers.parse('my account balance should be $"{expected_balance:d}"'))
def check_balance(expected_balance, logger):
    assert account['balance'] == int(expected_balance)
    logger.info('my account balance should be '+str(expected_balance)+', Actual: '+str(account["balance"])+'')

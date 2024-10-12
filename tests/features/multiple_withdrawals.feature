Feature: Multiple Withdrawals

  @multiple-withdrawal
  Scenario: Withdraw $10 from an account with sufficient funds
    Given I have an account with $"100" balance
    When I withdraw $"10"
    Then my account balance should be $"90"

  @multiple-withdrawal
  Scenario: Withdraw $20 from an account with sufficient funds
    Given I have an account with $"100" balance
    When I withdraw $"20"
    Then my account balance should be $"80"

  @multiple-withdrawal
  Scenario: Withdraw $30 from an account with sufficient funds
    Given I have an account with $"100" balance
    When I withdraw $"30"
    Then my account balance should be $"70"

  @multiple-withdrawal
  Scenario: Withdraw $40 from an account with sufficient funds
    Given I have an account with $"100" balance
    When I withdraw $"40"
    Then my account balance should be $"60"

  @multiple-withdrawal
  Scenario: Withdraw $50 from an account with sufficient funds
    Given I have an account with $"100" balance
    When I withdraw $"50"
    Then my account balance should be $"50"

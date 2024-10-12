.
├── features/
│   ├── banking_transactions.feature   # Contains deposit and withdrawal scenarios with markers
│   └── multiple_withdrawals.feature   # Contains 5 withdrawal scenarios
├── tests/
│   ├── test_banking.py                # Step definitions and test implementations
├── reports/                           # Folder to store test reports (HTML/JUnit)
├── conftest.py                        # Fixture management (empty for now)
├── pytest.ini                         # pytest configuration with markers and options
├── requirements.txt                   # List of Python dependencies
└── README.md                          # Project instructions and setup

python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

git clone https://github.com/your-repo/bdd-banking-tests.git
cd bdd-banking-tests

pip install -r requirements.txt

pytest

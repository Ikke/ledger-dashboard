## Enable flask debug mode. Don't enable this in production
#DEBUG = True

## Path to the binary. Searches PATH by default.
#LEDGER_BIN = '/path/to/ledger'

## Path to the ledger
LEDGER_FILE = "../data/demo.dat"

## Port where the webserver listens on
PORT = 5000

## Random key for securing cookies
SECRET_KEY= ""

## Ledger account names
class Accounts:
    ASSETS = "assets"
    ASSETS_PATTERN = "^Assets"

    INCOME = "income"
    INCOME_PATTERN = "^Income"

    EXPENSES = "expenses"
    EXPENSES_PATTERN = "^Expenses"

    LIABILITIES = "liabilities"
    LIABILITIES_PATTERN = "^Liabilities"


from pprint import pprint
import unittest
import sh
from ledgerdashboard.ledger.ledger import Ledger, regular_transactions


example_ledger = """
2014-01-01 Equity
  Equity:assets
  Assets:checking  $100.00

2014-01-02 Expense
  Expense:food  $10.00
  Assets:checking
"""


class LedgerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.ledger = Ledger(ledger_with_contents(example_ledger))

    def test_account_returns_defined_accounts(self):
        accounts = ["Assets:checking", "Equity:assets", "Expense:food"]

        returned_accounts = self.ledger.accounts()

        self.assertListEqual(accounts, returned_accounts)

    def test_balance_returns_correct_balance(self):
        result = self.ledger.balance()

        self.assertTupleEqual(("Assets:checking", "$", 90.00), result[0])

    def test_account_filter_returns_correct_balance(self):
        result = self.ledger.balance(accounts="Expense")
        self.assertTupleEqual(("Expense:food", "$", 10.00), result[0])


class RegularTransactionsTest(unittest.TestCase):
    def test_returns_multiple_tx_for_same_payee(self):
        txns = [
            {'date': '2014-10-14', "payee": "Bank A", "amount": 10.00},
            {'date': '2014-11-14', "payee": "Bank A", "amount": 10.00},
        ]

        result = regular_transactions(txns)
        self.assertEqual(1, len(result))

    def test_does_not_return_tx_with_different_amount(self):
        txns = [
            {'date': '2014-10-14', "payee": "Bank A", "amount": 10.00},
            {'date': '2014-11-14', "payee": "Bank A", "amount": 5.00},
        ]

        result = regular_transactions(txns)
        self.assertEqual(0, len(result))

    def test_canceled_payments_are_not_returned(self):
        txns = [
            {'date': '2014-05-14', "payee": "Bank A", "amount": 10.00},
            {'date': '2014-06-14', "payee": "Bank A", "amount": 10.00},
        ]

        result = regular_transactions(txns)
        self.assertEqual(0, len(result))


def ledger_with_contents(contents):
    return sh.Command('/usr/bin/ledger').bake(no_color=True, file="-", _in=contents)


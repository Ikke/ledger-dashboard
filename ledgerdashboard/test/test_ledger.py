from pprint import pprint
import unittest
import datetime
import sh
from ledgerdashboard.ledger.ledger import Ledger, find_recurring_transactions
from unittest_data_provider import data_provider


example_ledger = """
2014-01-01 Equity
  Equity:assets
  Assets:checking  $100.00

2014-01-02 Expense
  Expense:food  $10.00
  Assets:checking
"""


def nose_data_provider(dp_f):
    ndp_f = data_provider(dp_f)

    def wrapper(f):
        wrapped_function = ndp_f(f)
        wrapped_function.__name__ = f.__name__

        return wrapped_function

    return wrapper


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


class RecurringTransactionsTest(unittest.TestCase):
    def test_returns_multiple_tx_for_same_payee(self):
        txns = [
            {'date': '2014/09/14', "payee": "Bank A", "amount": 10.00},
            {'date': '2014/10/14', "payee": "Bank A", "amount": 10.00},
            {'date': '2014/11/14', "payee": "Bank A", "amount": 10.00},
        ]

        result = find_recurring_transactions(txns, datetime.datetime(2014, 11, 14))
        self.assertEqual(1, len(result))

    def test_does_not_return_3_transactions_with_different_amounts(self):
        txns = [
            {'date': '2014/09/14', "payee": "Bank A", "amount": 12.00},
            {'date': '2014/10/14', "payee": "Bank A", "amount": 10.00},
            {'date': '2014/11/14', "payee": "Bank A", "amount": 5.00},
        ]

        result = find_recurring_transactions(txns, datetime.datetime(2014, 11, 14))
        self.assertEqual(0, len(result))

    def test_does_return_3_transactions_with_one_different_amount(self):
        txns = [
            {'date': '2014/09/14', "payee": "Bank A", "amount": 10.00},
            {'date': '2014/10/14', "payee": "Bank A", "amount": 10.00},
            {'date': '2014/11/14', "payee": "Bank A", "amount": 5.00},
        ]

        result = find_recurring_transactions(txns, datetime.datetime(2014, 11, 14))
        self.assertEqual(1, len(result))

    def test_canceled_payments_are_not_returned(self):
        txns = [
            {'date': '2014/04/14', "payee": "Bank A", "amount": 10.00},
            {'date': '2014/05/14', "payee": "Bank A", "amount": 10.00},
            {'date': '2014/06/14', "payee": "Bank A", "amount": 10.00},
        ]

        result = find_recurring_transactions(txns, datetime.datetime(2014, 8, 15))
        self.assertEqual(0, len(result))

    txns_off_week_data = lambda: [[(
        {'date': '2014/04/14', "payee": "Bank A", "amount": 10.00},
        {'date': '2014/05/14', "payee": "Bank A", "amount": 10.00},
        {'date': '2014/06/21', "payee": "Bank A", "amount": 10.00},)
    ], [(
        {'date': '2014/04/28', "payee": "Bank A", "amount": 10.00},
        {'date': '2014/05/28', "payee": "Bank A", "amount": 10.00},
        {'date': '2014/07/02', "payee": "Bank A", "amount": 10.00},)
    ]]

    @nose_data_provider(txns_off_week_data)
    def test_payments_off_by_week_are_returned(self, txns):
        result = find_recurring_transactions(txns, datetime.datetime(2014, 7, 14))
        self.assertEqual(1, len(result))

    txns_longer_period_data = lambda: [[(
        {'date': '2014/01/04', "payee": "Bank A", "amount": 10.00},
        {'date': '2014/05/14', "payee": "Bank A", "amount": 10.00},
        {'date': '2014/09/25', "payee": "Bank A", "amount": 10.00},
    )]]

    @nose_data_provider(txns_longer_period_data)
    def test_multiple_transactions_over_longer_period_are_not_returned(self, txns):
        result = find_recurring_transactions(txns, datetime.datetime(2014, 10, 1))
        self.assertEqual(0, len(result))


def ledger_with_contents(contents):
    return sh.Command('/usr/bin/ledger').bake(no_color=True, file="-", _in=contents)

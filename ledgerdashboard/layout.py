from pprint import pprint
from flask import get_flashed_messages, url_for
import ledgerdashboard.settings as s


class Layout:
    def __init__(self):
        setattr(self, self.__class__.__name__.lower(), 'active')

    @staticmethod
    def message():
        messages = get_flashed_messages(category_filter=['message'])
        return messages[0] if len(messages) else None

    @staticmethod
    def error():
        errors = get_flashed_messages(category_filter=['error'])
        return errors[0] if len(errors) else None


class Dashboard(Layout):
    def __init__(self):
        self.accounts = []
        self.income = []
        self.expense_balances = []
        self.expenses_previous_month = []
        self.last_expenses = []
        super().__init__()

    def expenses_present(self):
        try:
            return len(self.expense_balances) > 0
        except AttributeError:
            return False


class Expenses(Layout):
    def __init__(self, form_data=None):
        if form_data:
            for name, value in form_data.items():
                setattr(self, name, value)

        if not hasattr(self, 'date'):
            self.date = self.today()

        self.api_expense_accounts_url = url_for('api_accounts', account_filter=s.Accounts.EXPENSES)
        self.api_accounts_url = url_for('api_accounts')

        super().__init__()

    @staticmethod
    def today():
        from datetime import date
        return date.today().strftime("%Y-%m-%d")
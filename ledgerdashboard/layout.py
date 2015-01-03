from pprint import pprint
from flask import get_flashed_messages


class Layout:
    def __init__(self):
        setattr(self, self.__class__.__name__.lower(), 'active')

    def message(self):
        messages = get_flashed_messages(category_filter=['message'])
        return messages[0] if len(messages) else None

    def error(self):
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
        pprint(form_data)
        if form_data:
            for name, value in form_data.items():
                setattr(self, name, value)

        if not hasattr(self, 'date'):
            self.date = self.today()

        super().__init__()

    def today(self):
        from datetime import date
        return date.today().strftime("%Y-%m-%d")
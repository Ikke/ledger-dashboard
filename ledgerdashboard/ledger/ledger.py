import re
import sh
import csv
from pprint import pprint
import ledgerdashboard.settings as settings
import os.path
import locale

class Ledger:
    def __init__(self, command, filename=""):
        self.ledger = command
        self.filename = filename
        self._aliases = {}

    @classmethod
    def new(cls, filename):
        if hasattr(settings, 'LEDGER_BIN'):
            ledger_bin = settings.LEDGER_BIN
        else:
            ledger_bin = sh.which('ledger')

        if not os.path.exists(ledger_bin):
            raise ValueError("Ledger binary not found at: {}".format(ledger_bin))

        return Ledger(sh.Command(ledger_bin).bake(_tty_out=False, no_color=True, file=filename), filename=filename)

    def accounts(self, account_filter=""):
        result = self.ledger.accounts(account_filter)
        return [account for account in result.split("\n") if account]

    def balance(self, accounts=None, **kwargs):

        pattern = re.compile("([A-Za-z0-9:]+) ([A-Z]{3}|[$€£]) *([-0-9.,]+)")
        balance_output = self._command(
            command="balance",
            accounts=accounts,
            balance_format="%A %(display_total)\n%/",
            _debug=False,
            **kwargs
        )

        balances = []
        for balance in balance_output.strip().split("\n"):
            if not balance:
                continue
            match = pattern.search(balance)
            if match:
                balances.append((match.group(1), match.group(2), locale.atof(match.group(3))))

        return balances

    def register(self, accounts=None, **kwargs):
        register = self._command('csv', accounts, **kwargs)
        reader = csv.DictReader(register.split("\n"), ["date", "code", "payee", "account", "currency", "amount", "cost", "note"])

        return list(reader)

    def aliases(self):
        import re

        if self._aliases:
            return self._aliases

        pattern = re.compile("alias ([^=]+)=(.+)")
        f = open(self.filename)
        for line in f.read().split("\n"):
            match = pattern.search(line)
            if match:
                alias = match.group(1).strip()
                value = match.group(2).strip()
                self._aliases[alias] = value

        return self._aliases

    def make_aliased(self, account):
        aliases = self.aliases()
        for alias, value in aliases.items():
            account = account.replace(value, alias)
        return account

    def _command(self, command, accounts=None, _debug=False, **kwargs):
        args = list()

        if accounts:
            args.extend(accounts.split(" "))

        ledger_command = self.ledger.bake(command, *args, **kwargs)

        if _debug:
            print(ledger_command)

        return ledger_command()


class LedgerWriter:
    def __init__(self, filename):
        self.filename = filename

    def write_expense(self, posting):
        posting_text = "\n{date:} {payee:}\n".format(**posting)
        if posting['description']:
            posting_text += "    ;{description}\n".format(**posting)

        posting_text += "    {account: <40s}{currency}{amount: >8s}\n".format(**posting)

        if posting['use_source']:
            posting_text += "    {source_account:}".format(**posting)

        posting_text += "\n"

        with open(self.filename, 'a') as ledger_file:
            ledger_file.write(posting_text)


from collections import defaultdict, Counter
from datetime import datetime


def find_recurring_transactions(transactions, current_date):
    groups = defaultdict(list)
    for tx in transactions:
        groups[tx['payee']].append(tx)

    multiple = [item for _, item in groups.items() if len(item) > 1]

    same_amount = []
    for group in multiple:
        last_txns = sorted(group, key=lambda txn: txn['date'], reverse=False)[-3:]

        amounts = Counter()

        amounts.update(item['amount'] for item in last_txns)

        _, nr_same = amounts.most_common(1)[0]

        if nr_same == 3 or (nr_same == 2 and len(last_txns) == 3):
            first_txn = last_txns[0]
            last_txn = last_txns[-1]

            if (current_date - datetime.strptime(last_txn['date'], "%Y/%m/%d")).days < 40 \
                    and (current_date - datetime.strptime(first_txn['date'], "%Y/%m/%d")).days < 120:
                same_amount.append(last_txns[-1])

    return same_amount

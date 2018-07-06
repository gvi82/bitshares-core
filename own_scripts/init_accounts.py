#!/usr/bin/python3

from wallet import Wallet

w = Wallet('ws://158.69.224.80:33001', False, 'nathan', '5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3', None, None, 'BTS')
w.unlock("123")
w.import_key2()
w.get_balance("nathan")

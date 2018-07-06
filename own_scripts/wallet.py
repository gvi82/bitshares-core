import hashlib
import json

import base58
from websocket import create_connection

perm = {}
perm["charge_market_fee"] = 0x01
perm["white_list"] = 0x02
perm["override_authority"] = 0x04
perm["transfer_restricted"] = 0x08
perm["disable_force_settle"] = 0x10
perm["global_settle"] = 0x20
perm["disable_confidential"] = 0x40
perm["witness_fed_asset"] = 0x80
perm["committee_fed_asset"] = 0x100


class Wallet:

    def __init__(self, url, is_verbose, base_account, base_account_key, money_account, money_account_key, base_asset):
        self.id = 1
        self.ws = create_connection(url)
        self.is_verbose = is_verbose
        self.base_account = base_account
        self.base_account_key = base_account_key
        self.money_account = money_account
        self.money_account_key = money_account_key

        if self.money_account is None:
            self.money_account = base_account
            self.money_account_key = money_account_key

        self.base_asset = base_asset

    def call(self, command):
        command["id"] = self.id
        self.id = self.id + 1
        if self.is_verbose:
            print("Send: ", command)
        self.ws.send(json.dumps(command))
        result = self.ws.recv()
        if self.is_verbose:
            print("Recv: ", result)
        return json.loads(result)

    def call_simple(self, command_name, parameters):
        command = {"method": "call", "params": [0, command_name, [ parameters ] ]}
        return self.call(command)

    def create_account(self, account, password):
        command = {"method": "call", "params": [0, "create_account_with_password",
                                                [password, account, self.base_account, self.base_account, True,
                                                 True]]}
        self.call(command)


    def create_account_with_money(self, account, password, money):
        command = {"method": "call", "params": [0, "create_account_with_password",
                                                [password, account, self.base_account, self.base_account, True,
                                                 True]]}
        result = self.call(command)
        if 'result' in result:
            command = {"method": "call", "params": [0, "transfer", [self.money_account, account, money, self.base_asset,
                                                                    self.base_asset, True]]}
            self.call(command)

    def transfer(self, account, money):
        command = {"method": "call", "params": [0, "transfer", [self.money_account, account, money, self.base_asset,
                                                                self.base_asset, True]]}
        self.call(command)

    def unlock(self, pswd):
        result = self.call({"method": "call", "params": [0, "is_new", []]})
        if result['result']:
            self.call({"method": "call", "params": [0, "set_password", [pswd]]})

        result = self.call({"method": "call", "params": [0, "is_locked", []]})
        if result['result']:
            self.call({"method": "call", "params": [0, "unlock", [pswd]]})

    def import_key2(self):
        if self.base_account is not None:
            self.import_key(self.base_account, self.base_account_key)

        if self.money_account is not None:
            self.import_key(self.money_account, self.money_account_key)

    def import_key(self, account, wif_priv_key):
        self.call({"method": "call", "params": [0, "import_key", [account, wif_priv_key]]})
        self.call({"method": "call", "params": [0, "import_balance", [account, [wif_priv_key], True]]})

    def import_key_by_password(self, account, password):
        priv_key = hashlib.sha256(bytes(bytearray(account + "active" + password, 'utf-8'))).digest()
        h = b'\x80' + priv_key
        h += hashlib.sha256(hashlib.sha256(h).digest()).digest()[:4]
        wif_priv_key = base58.b58encode(h)
        self.import_key(account, wif_priv_key)

    def get_balance(self, account):
        res = self.call({"method": "call", "params": [0, "list_account_balances", [account]]})
        print(account,"ballance:",res["result"])

    def create_asset(self, account, symb):
        permissions = {"charge_market_fee" : True,
                       "white_list" : True,
                       "override_authority" : True,
                       "transfer_restricted" : True,
                       "disable_force_settle" : False,
                       "global_settle" : False,
                       "disable_confidential" : True,
                       "witness_fed_asset" : True,
                       "committee_fed_asset" : True,
                      }
        flags       = {"charge_market_fee" : False,
                       "white_list" : False,
                       "override_authority" : False,
                       "transfer_restricted" : False,
                       "disable_force_settle" : False,
                       "global_settle" : False,
                       "disable_confidential" : False,
                       "witness_fed_asset" : False,
                       "committee_fed_asset" : False,
                      }

        permissions_int = 0
        for p in permissions :
            if permissions[p]:
                permissions_int += perm[p]
        flags_int = 0
        for p in permissions :
            if flags[p]:
                flags_int += perm[p]
        options = {"max_supply" : 1000000000000000,
                   "market_fee_percent" : 0,
                   "max_market_fee" : 0,
                   "issuer_permissions" : permissions_int,
                   "flags" : flags_int,
                   "core_exchange_rate" : {
                       "base": {
                           "amount": 1,
                           "asset_id": "1.3.0"},
                       "quote": {
                           "amount": 1,
                           "asset_id": "1.3.1"}},
                   "whitelist_authorities" : [],
                   "blacklist_authorities" : [],
                   "whitelist_markets" : [],
                   "blacklist_markets" : [],
                   "description" : "My fancy description"
                   }

        res = self.call({"method": "call", "params": [0, "create_asset", [account,symb,3,options,None,True]]})
        print(res)

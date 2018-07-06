#!/usr/bin/python3

from wallet import Wallet

w = Wallet('ws://127.0.0.1:8091', False, 'totalpoker', '5JWG1iDp3NzXvPseQrst5LALskWc8e32Km6JPkiH7xBXeT81Qbb', None, None, 'PLC')
#w.unlock("123")
#w.import_key2()
w.create_asset("totalpoker", "GVIT")
w.get_balance('totalpoker')

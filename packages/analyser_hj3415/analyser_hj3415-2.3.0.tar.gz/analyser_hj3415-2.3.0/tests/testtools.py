import unittest
from analyser_hj3415 import tools
from db_hj3415 import mongo
import math


class EvalToolsTests(unittest.TestCase):
    def setUp(self):
        self.addr = "mongodb://hj3415:piyrw421@192.168.100.175:27017/"
        self.client = mongo.connect_mongo(self.addr)
        mongo.Base.initialize_client(self.client)
        self.test_codes = mongo.Corps.list_all_codes()

    def tearDown(self):
        self.client.close()

    def test_set_data(self):
        tester = ['2023/03', '2023/03', '2023/06', '2024/09', '', math.nan, None]
        print(tools.set_data(*tester))

    def test_calc당기순이익(self):
        for code in self.test_codes:
            print(code, tools.calc당기순이익(code))

    def test_calc유동자산(self):
        for code in self.test_codes:
            print(code, tools.calc유동자산(code))

    def test_calc유동부채(self):
        for code in self.test_codes:
            print(code, tools.calc유동부채(code))

    def test_calc비유동부채(self):
        # 예수부채를 사용하는 보험사계열
        code = '000370'
        for code in self.test_codes:
            print(code, tools.calc비유동부채(code))

    def test_calc유동비율(self):
        for code in self.test_codes:
            print(code, tools.calc유동비율(code, pop_count=2))

    def test_findFCF(self):
        for code in self.test_codes:
            fcf_dict = tools.findFCF(code)
            print(code, fcf_dict, mongo.C1034.latest_dict_value(fcf_dict))

    def test_getmarketcap(self):
        for code in self.test_codes:
            print(code, tools.get_marketcap(code))

    def test_findPFCF(self):
        for code in self.test_codes:
            pfcf_dict = tools.findPFCF(code)
            print(code, pfcf_dict, mongo.C1034.latest_dict_value(pfcf_dict))




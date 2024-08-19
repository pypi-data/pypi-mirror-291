import unittest
import pprint
import random
from db_hj3415 import cli, myredis
print("테스트용 서버로 주소 설정")
cli.save_mongo_addr('mongodb://hj3415:piyrw421@192.168.100.175:27017')
cli.save_redis_addr('192.168.100.175')
from analyser_hj3415.analysers import eval


class EvalTests(unittest.TestCase):
    def setUp(self):
        self.test_codes = myredis.Corps.list_all_codes()

    def tearDown(self):
        pass

    def test_red(self):
        test_one = random.choice(self.test_codes)
        print(test_one, '/', myredis.Corps.get_name(test_one))
        pprint.pprint(eval.red(test_one))

        print(test_one, '/', myredis.Corps.get_name(test_one))
        pprint.pprint(eval.red(test_one))

    def test_red_all(self):
        print(f'Totol {len(self.test_codes)} items')
        for i, code in enumerate(self.test_codes):
            print(i, '/', code, '/', myredis.Corps.get_name(code))
            print(eval.red(code))
        import time
        time.sleep(2)
        print(f'Totol {len(self.test_codes)} items')
        for i, code in enumerate(self.test_codes):
            print(i, '/', code, '/', myredis.Corps.get_name(code))
            print(eval.red(code))

    def test_mil(self):
        test_one = random.choice(self.test_codes)
        print(test_one, '/', myredis.Corps.get_name(test_one))
        pprint.pprint(eval.mil(test_one))

        print(test_one, '/', myredis.Corps.get_name(test_one))
        pprint.pprint(eval.mil(test_one))

    def test_mil_all(self):
        print(f'Totol {len(self.test_codes)} items')
        for i, code in enumerate(self.test_codes):
            print(i, '/', code, '/', myredis.Corps.get_name(code))
            print(eval.mil(code))

        import time
        time.sleep(2)
        print(f'Totol {len(self.test_codes)} items')
        for i, code in enumerate(self.test_codes):
            print(i, '/', code, '/', myredis.Corps.get_name(code))
            print(eval.mil(code))

    def test_blue(self):
        test_one = random.choice(self.test_codes)
        print(test_one, '/', myredis.Corps.get_name(test_one))
        pprint.pprint(eval.blue(test_one))

        print(test_one, '/', myredis.Corps.get_name(test_one))
        pprint.pprint(eval.blue(test_one))

    def test_blue_all(self):
        print(f'Totol {len(self.test_codes)} items')
        for i, code in enumerate(self.test_codes):
            print(i, '/', code, '/', myredis.Corps.get_name(code))
            print(eval.blue(code))

        import time
        time.sleep(2)
        print(f'Totol {len(self.test_codes)} items')
        for i, code in enumerate(self.test_codes):
            print(i, '/', code, '/', myredis.Corps.get_name(code))
            print(eval.blue(code))

    def test_growth(self):
        test_one = random.choice(self.test_codes)
        print(test_one, '/', myredis.Corps.get_name(test_one))
        pprint.pprint(eval.growth(test_one))

        print(test_one, '/', myredis.Corps.get_name(test_one))
        pprint.pprint(eval.growth(test_one))

    def test_growth_all(self):
        print(f'Totol {len(self.test_codes)} items')
        for i, code in enumerate(self.test_codes):
            print(i, '/', code, '/', myredis.Corps.get_name(code))
            print(eval.growth(code))

        import time
        time.sleep(2)
        print(f'Totol {len(self.test_codes)} items')
        for i, code in enumerate(self.test_codes):
            print(i, '/', code, '/', myredis.Corps.get_name(code))
            print(eval.growth(code))

    def test_eval_all(self):
        pp = pprint.PrettyPrinter(width=200)
        print(f'Totol {len(self.test_codes)} items')
        for i, code in enumerate(self.test_codes):
            print(i, '/', code, '/', myredis.Corps.get_name(code))
            print(eval.red(code))
            pp.pprint(eval.mil(code))
            pp.pprint(eval.blue(code))
            pprint.pprint(eval.growth(code), width=150)


import unittest
import random

from db_hj3415 import cli, myredis
print("테스트용 서버로 주소 설정")
cli.save_mongo_addr('mongodb://hj3415:piyrw421@192.168.100.175:27017')
cli.save_redis_addr('192.168.100.175')

from analyser_hj3415.analysers import score


class ScoreTests(unittest.TestCase):
    def setUp(self):
        self.test_codes = myredis.Corps.list_all_codes()

    def tearDown(self):
        pass

    def test_red(self):
        test_one = random.choice(self.test_codes)
        print(test_one, '/', myredis.Corps.get_name(test_one))
        print(score.red(test_one))

    def test_red_all(self):
        print(f'Totol {len(self.test_codes)} items')
        for i, code in enumerate(self.test_codes):
            print(i, '/', code, '/', myredis.Corps.get_name(code))
            print(score.red(code))

    def test_mil(self):
        test_one = random.choice(self.test_codes)
        print(test_one, '/', myredis.Corps.get_name(test_one))
        print(score.mil(test_one))

    def test_mil_all(self):
        print(f'Totol {len(self.test_codes)} items')
        for i, code in enumerate(self.test_codes):
            print(i, '/', code, '/', myredis.Corps.get_name(code))
            print(score.mil(code))

    def test_blue(self):
        test_one = random.choice(self.test_codes)
        print(test_one, '/', myredis.Corps.get_name(test_one))
        p1, p2, p3, p4, p5 = score.blue(test_one)
        print(test_one, "유동비율", p1, "이자보상배율", p2, "순부채비율", p3, "순운전자본회전율", p4, "재고자산회전율", p5)

    def test_blue_all(self):
        print(f'Totol {len(self.test_codes)} items')
        for i, code in enumerate(self.test_codes):
            print(i, '/', code, '/', myredis.Corps.get_name(code))
            p1, p2, p3, p4, p5 = score.blue(code)
            print(code, "유동비율", p1, "이자보상배율", p2, "순부채비율", p3, "순운전자본회전율", p4, "재고자산회전율", p5)

    def test_growth_one(self):
        test_one = random.choice(self.test_codes)
        print(test_one, '/', myredis.Corps.get_name(test_one))
        p1, p2 = score.growth(test_one)
        print(test_one, "매출액증가율", p1, "영업이익률", p2)

    def test_growth_all(self):
        print(f'Totol {len(self.test_codes)} items')
        for i, code in enumerate(self.test_codes):
            print(i, '/', code, '/', myredis.Corps.get_name(code))
            p1, p2 = score.growth(code)
            print(code, "매출액증가율", p1, "영업이익률", p2)

    def test_one(self):
        test_one = random.choice(self.test_codes)
        name = myredis.Corps.get_name(test_one)
        print('/'.join([str(1), str(test_one), str(name)]))
        print('red', score.red(test_one))
        print('mil', score.mil(test_one))
        print('blue', score.blue(test_one))
        print('growth', score.growth(test_one))

    def test_all(self):
        for i, test_one in enumerate(self.test_codes):
            name = myredis.Corps.get_name(test_one)
            print('/'.join([str(i+1), str(test_one), str(name)]))
            print('red', score.red(test_one))
            print('mil', score.mil(test_one))
            print('blue', score.blue(test_one))
            print('growth', score.growth(test_one))


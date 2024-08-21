import time
import unittest
import pprint
import random
from analyser_hj3415 import myredis
from db_hj3415 import cli
from db_hj3415.myredis import Corps
print("테스트용 서버로 주소 설정")
cli.save_mongo_addr('mongodb://hj3415:piyrw421@192.168.100.175:27017')
cli.save_redis_addr('192.168.100.175')


class MyredisTests(unittest.TestCase):
    def setUp(self):
        self.test_codes = Corps.list_all_codes()

    def tearDown(self):
        pass

    def test_red_n_score(self):
        test_one = random.choice(self.test_codes)
        print(test_one, '/', Corps.get_name(test_one))
        pprint.pprint(myredis.red_n_score(test_one))

        time.sleep(2)

        print(test_one, '/', Corps.get_name(test_one))
        pprint.pprint(myredis.red_n_score(test_one))

    def test_mil_n_score(self):
        test_one = random.choice(self.test_codes)
        print(test_one, '/', Corps.get_name(test_one))
        pprint.pprint(myredis.mil_n_score(test_one))

        time.sleep(2)

        print(test_one, '/', Corps.get_name(test_one))
        pprint.pprint(myredis.mil_n_score(test_one))

    def test_blue_n_score(self):
        test_one = random.choice(self.test_codes)
        print(test_one, '/', Corps.get_name(test_one))
        pprint.pprint(myredis.blue_n_score(test_one))

        time.sleep(2)

        print(test_one, '/', Corps.get_name(test_one))
        pprint.pprint(myredis.blue_n_score(test_one))

    def test_growth_n_score(self):
        test_one = random.choice(self.test_codes)
        print(test_one, '/', Corps.get_name(test_one))
        pprint.pprint(myredis.growth_n_score(test_one))

        time.sleep(2)

        print(test_one, '/', Corps.get_name(test_one))
        pprint.pprint(myredis.growth_n_score(test_one))

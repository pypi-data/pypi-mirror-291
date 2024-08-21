import pprint
import unittest
import random

from db_hj3415 import cli, myredis
print("테스트용 서버로 주소 설정")
cli.save_mongo_addr('mongodb://hj3415:piyrw421@192.168.100.175:27017')
cli.save_redis_addr('192.168.100.175')

from analyser_hj3415.analysers.report import Report


class ReportTest(unittest.TestCase):
    def setUp(self):
        self.test_codes = myredis.Corps.list_all_codes()

    def tearDown(self):
        pass

    def test_Report(self):
        test_one = random.choice(self.test_codes)
        print(test_one, '/', myredis.Corps.get_name(test_one))
        print(Report(client, self.rndcode))

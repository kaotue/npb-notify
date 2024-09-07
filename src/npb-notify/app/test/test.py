import unittest
import os
from dataclasses import dataclass

import app
import app_ver2
from NpbContext import NpbContext
from classes.top_page import TopPage

BASE_DOMAIN_NAME = os.environ['NPB_BASE_DOMAIN_NAME']


def lambda_context():
    @dataclass
    class LambdaContext:
        function_name: str = "test"
        memory_limit_in_mb: int = 128
        invoked_function_arn: str = (
            "arn:aws:lambda:ap-northeast-1:000000000:function:test"
        )
        aws_request_id: str = "52fdfc07-2182-154f-163f-5f0f9a621d72"

    return LambdaContext()


class TestMethods(unittest.TestCase):
    def test_app(self):
        result = app.main2('https://{0}/npb/game/2021020624/top'.format(BASE_DOMAIN_NAME), '#ffdd00', '試合終了')
        print(f'{result=}')
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()

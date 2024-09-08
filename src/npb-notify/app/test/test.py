import unittest
import os
from dataclasses import dataclass

import app
from npb_context import NpbContext
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
    # def test_app(self):
    #     context = NpbContext(top_url='https://{0}/npb/teams/5/top'.format(BASE_DOMAIN_NAME),
    #                          color='#ffdd00')
    #     top_page = TopPage(game_page_url='https://{0}/npb/game/2021020624/top'.format(BASE_DOMAIN_NAME),
    #                        game_status='試合終了')
    #     result = app.main2(context, top_page)
    #     print(f'{result=}')
    #     self.assertEqual(True, True)

    def test_lambda_handler(self):
        result = app.lambda_handler(None, lambda_context())
        print(f'{result=}')
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()

import os
import slack
from npb_context import NpbContext
from classes.top_page import TopPage
from selects.top_page_selector import TopPageSelector
from selects.game_selector import GameSelector


INTERVAL_SECONDS = float(os.getenv('INTERVAL_SECONDS', 1.5))
BASE_DOMAIN_NAME = os.environ['NPB_BASE_DOMAIN_NAME']
TOP_URLS = os.getenv('TOP_URLS',
                     'https://{0}/npb/teams/5/top,'
                     'https://{0}/npb/teams/3/top,'
                     'https://{0}/npb/teams/376/top'
                     ).format(BASE_DOMAIN_NAME).split(',')
TEAM_COLORS = os.getenv('TEAM_COLORS',
                        '#ffdd00,'
                        '#0096e0,'
                        '#940028'
                        ).split(',')

IS_DEVELOPMENT = os.getenv('IS_DEVELOPMENT', 'True').lower() == 'true'


def lambda_handler(event, context):
    for top_url, color in zip(TOP_URLS, TEAM_COLORS):
        npb_context = NpbContext(top_url=top_url, color=color)
        if not main1(npb_context):
            continue
    return True


def main1(context):
    # トップページから本日の試合情報と試合URLを取得
    top_page = TopPageSelector(context.top_url).select()
    if not top_page.game_status:
        return False
    print(f'{top_page.game_status=}')
    if top_page.game_status == '試合なし' or top_page.game_status == '試合終了':
        return True
    top_page.game_page_url = top_page.game_page_url.replace('index', 'top')
    return main2(context, top_page)


def main2(context: NpbContext, top_page: TopPage):
    game = GameSelector(top_page.game_page_url).select()
    slack.push(game.get_notify_header(), game.get_notify_message(), context.color)
    return True


if __name__ == '__main__':
    lambda_handler(None, None)

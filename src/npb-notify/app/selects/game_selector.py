import os
import utils
from bs4 import BeautifulSoup
from selects.base_selector import BaseSelector
from selects.pitcher_selector import PitcherSelector
from selects.batter_selector import BatterSelector
from classes.game import Game
from classes.team import Team
from classes.batter import Batter


BASE_DOMAIN_NAME = os.environ['NPB_BASE_DOMAIN_NAME']


def get_pitcher_url(html, team_num):
    soup = BeautifulSoup(html, 'html.parser')
    a = soup.select_one(
        f'#strt_mem > section > div > section:nth-child({team_num}) > table:nth-child(2) > tbody > tr > td.bb-splitsTable__data.bb-splitsTable__data--text > a')
    if not a:
        return None
    return f"https://{BASE_DOMAIN_NAME}{a.get('href')}"


def get_batters(html, team_num):
    soup = BeautifulSoup(html, 'html.parser')
    rows = soup.select(
        f'#strt_mem > section > div > section:nth-child({team_num}) > table:nth-child(3) > tbody > tr')
    batters = []
    if not rows:
        return None
    for row in rows:
        batter = Batter(
            打順=row.select_one(f'td:nth-child(1)').get_text(),
            位置=row.select_one(f'td:nth-child(2)').get_text(),
            選手名=row.select_one(f'td:nth-child(3) > a').get_text(),
            打=row.select_one(f'td:nth-child(4)').get_text(),
            打率=utils.conv_ave(row.select_one(f'td:nth-child(5)').getText()),
            link=f"https://{BASE_DOMAIN_NAME}{row.select_one(f'td:nth-child(3) > a').get('href')}",
        )
        batter = BatterSelector(url=batter.link).select(batter)
        batters.append(batter)
        print(f'{batter=}')
    return batters


class GameSelector(BaseSelector):
    def select(self) -> Game:
        html = self.download()
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.select_one(f'#async-gameCard').get_text().replace(' ', '').replace('\n', ' ').strip()
        team_name_a = soup.select_one('#async-gameDetail > div:nth-child(1) > p > a').get_text()
        team_name_b = soup.select_one('#async-gameDetail > div:nth-child(3) > p > a').get_text()
        status = soup.select_one('#async-gameDetail > div.bb-gameTeam__score > p.bb-gameCard__state').get_text().strip()
        return Game(
            link=self.url,
            title=title,
            home_team=Team(
                name=team_name_a,
                pitcher=PitcherSelector(url=get_pitcher_url(html, 1)).select(),
                batters=get_batters(html, 1)
            ),
            away_team=Team(
                name=team_name_b,
                pitcher=PitcherSelector(url=get_pitcher_url(html, 2)).select(),
                batters=get_batters(html, 2)
            ),
            date='',
            status=status,
            stadium='',
            home_score=0,
            away_score=0
        )

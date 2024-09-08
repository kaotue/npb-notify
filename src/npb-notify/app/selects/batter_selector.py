import utils
from datetime import datetime
from bs4 import BeautifulSoup
from selects.base_selector import BaseSelector
from classes.batter_recent_stats import BatterRecentStats


class BatterSelector(BaseSelector):
    def select(self, batter):
        if not (html := self.download()):
            return None
        html = self.download()
        soup = BeautifulSoup(html, 'html.parser')
        header_title = soup.select_one('#js-tabDom01 > section:nth-child(1) > header > h2').get_text().strip()
        if header_title == '打者成績':
            batter.本塁打 = soup.select_one('#js-tabDom01 > section:nth-child(1) > table > tbody > tr:nth-child(2) > td:nth-child(8)').get_text()
        else:
            batter.本塁打 = soup.select_one('#js-tabDom01 > section:nth-child(2) > table > tbody > tr:nth-child(2) > td:nth-child(8)').get_text()
        rows = soup.select(f'#game_b > tbody > tr')
        recent_stats = []
        for row in rows:
            recent_stats.append(
                BatterRecentStats(
                    日付=utils.conv_date(row.select_one(f'td:nth-child(1) > a').get_text()),
                    対戦チーム=row.select_one(f'td:nth-child(2)').get_text(),
                    打数=row.select_one(f'td:nth-child(3)').get_text(),
                    安打=row.select_one(f'td:nth-child(4)').get_text(),
                    本塁打=row.select_one(f'td:nth-child(5)').getText(),
                    打点=row.select_one(f'td:nth-child(6)').getText(),
                    得点=row.select_one(f'td:nth-child(7)').getText(),
                    三振=row.select_one(f'td:nth-child(8)').getText(),
                    四球=row.select_one(f'td:nth-child(9)').getText(),
                    死球=row.select_one(f'td:nth-child(10)').getText(),
                    打席結果=row.select_one(f'td:nth-child(11)').getText(),
                )
            )
        batter.RecentStats = recent_stats
        return batter

from datetime import datetime
from bs4 import BeautifulSoup
from selects.base_selector import BaseSelector
from classes.pitcher import Pitcher
from classes.pitcher_recent_stats import PitcherRecentStats


class PitcherSelector(BaseSelector):
    def select(self) -> Pitcher:
        html = self.download()
        soup = BeautifulSoup(html, 'html.parser')
        pitcher = Pitcher()
        pitcher.link = self.url
        pitcher.選手名 = soup.select_one('#contentMain > div.bb-centerColumn > div.bb-modCommon01 > div > div > div.bb-profile__data > ruby > h1').get_text().strip()
        pitcher.防御率 = soup.select_one('#js-tabDom01 > section:nth-child(1) > table > tbody > tr:nth-child(2) > td:nth-child(1)').get_text()
        pitcher.勝利 = soup.select_one('#js-tabDom01 > section:nth-child(1) > table > tbody > tr:nth-child(2) > td:nth-child(8)').get_text()
        pitcher.敗戦 = soup.select_one('#js-tabDom01 > section:nth-child(1) > table > tbody > tr:nth-child(2) > td:nth-child(9)').get_text()
        rows = soup.select(f'#game_p > tbody > tr')
        recent_stats = []
        for row in rows:
            recent_stats.append(
                PitcherRecentStats(
                    日付=datetime.strptime(row.select_one(f'td:nth-child(1) > a').get_text(), "%m月%d日").date(),
                    対戦チーム=row.select_one(f'td:nth-child(2)').get_text(),
                    登板=row.select_one(f'td:nth-child(3)').get_text(),
                    結果=row.select_one(f'td:nth-child(4)').get_text(),
                    投球回=row.select_one(f'td:nth-child(5)').getText(),
                    投球数=row.select_one(f'td:nth-child(6)').getText(),
                    打者=row.select_one(f'td:nth-child(7)').getText(),
                    被安打=row.select_one(f'td:nth-child(8)').getText(),
                    被本塁打=row.select_one(f'td:nth-child(9)').getText(),
                    奪三振=row.select_one(f'td:nth-child(10)').getText(),
                    与四球=row.select_one(f'td:nth-child(11)').getText(),
                    与死球=row.select_one(f'td:nth-child(12)').getText(),
                    暴投=row.select_one(f'td:nth-child(13)').getText(),
                    ボーク=row.select_one(f'td:nth-child(14)').getText(),
                    失点=row.select_one(f'td:nth-child(15)').getText(),
                    自責点=row.select_one(f'td:nth-child(16)').getText(),
                )
            )
        pitcher.RecentStats = recent_stats
        return pitcher

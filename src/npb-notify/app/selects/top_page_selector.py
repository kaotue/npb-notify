from bs4 import BeautifulSoup
from selects.batter_selector import BaseSelector
from classes.top_page import TopPage


class TopPageSelector(BaseSelector):
    def select(self) -> TopPage:
        html = self.download()
        soup = BeautifulSoup(html, 'html.parser')
        a = soup.select_one(
            '#wk_sche > section > table > tbody > tr > td.bb-calendarTable__data.bb-calendarTable__data--today > div > div.bb-calendarTable__wrap > a')
        if not a:
            return TopPage(
                game_status='',
                game_page_url='')
        return TopPage(
            game_status=a.get_text(),
            game_page_url=a.get('href'))

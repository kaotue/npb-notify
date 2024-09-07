import os
import time
import urllib.request
import slack
from bs4 import BeautifulSoup

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


def download_html(url):
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as res:
        html = res.read()
        time.sleep(INTERVAL_SECONDS)
        return html


def lambda_handler(event, context):
    for top_url, rgb in zip(TOP_URLS, TEAM_COLORS):
        if not main1(top_url, rgb):
            continue
    return True


def main1(top_url, rgb):
    # トップページから本日の試合情報と試合URLを取得
    (game_status, game_url) = get_game_status_and_url(top_url)
    if not game_status:
        return False
    print(f'{game_status=}')
    if game_status == '試合なし' or game_status == '試合終了':
        return True
    game_url = game_url.replace('index', 'top')

    return main2(game_url, rgb, game_status)


def main2(game_url, rgb, game_status):
    if not (game_html := download_html(game_url)):
        return False

    game = get_game(game_html, game_status, game_url)

    if pitcher_a := get_pitcher_info(game_html, 1):
        pitcher_a['直近'] = get_pitcher_past_record(pitcher_a)
    if players_a := get_players(game_html, 1):
        for player in players_a:
            player['直近'] = get_past_record(player)
            if IS_DEVELOPMENT:
                print(player)

    if pitcher_b := get_pitcher_info(game_html, 2):
        pitcher_b['直近'] = get_pitcher_past_record(pitcher_b)
    if players_b := get_players(game_html, 2):
        for player in players_b:
            player['直近'] = get_past_record(player)
            if IS_DEVELOPMENT:
                print(player)

    team_a = {
        'pitcher': pitcher_a,
        'batters': players_a,
    }
    team_b = {
        'pitcher': pitcher_b,
        'batters': players_b,
    }

    # Slackに通知
    slack.push(create_title(game), create_message(game, team_a, team_b), rgb)
    return True


def get_game_status_and_url(team_top_url):
    html = download_html(team_top_url)
    soup = BeautifulSoup(html, 'html.parser')
    a = soup.select_one('#wk_sche > section > table > tbody > tr > td.bb-calendarTable__data.bb-calendarTable__data--today > div > div.bb-calendarTable__wrap > a')
    if not a:
        return (None, None)
    text = a.get_text()
    href = a.get('href')
    return (text, href)


def get_title(html, game_status, game_url):
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.select_one(f'#async-gameCard').get_text().replace(' ', '').replace('\n', ' ').strip()
    team_name_a = soup.select_one('#async-gameDetail > div:nth-child(1) > p > a').get_text()
    team_name_b = soup.select_one('#async-gameDetail > div:nth-child(3) > p > a').get_text()
    return f"*{title}*\n*{team_name_a} vs {team_name_b}*\n<{game_url}|{game_status}>"


def get_game(html, game_status, game_url):
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.select_one(f'#async-gameCard').get_text().replace(' ', '').replace('\n', ' ').strip()
    team_name_a = soup.select_one('#async-gameDetail > div:nth-child(1) > p > a').get_text()
    team_name_b = soup.select_one('#async-gameDetail > div:nth-child(3) > p > a').get_text()
    return {
        'title': title,
        'team_name_a': team_name_a,
        'team_name_b': team_name_b,
        'link': game_url,
        'status': game_status,
    }


# 先発投手情報の取得
def get_pitcher_info(html, team_num):
    soup = BeautifulSoup(html, 'html.parser')
    a = soup.select_one(
        f'#strt_mem > section > div > section:nth-child({team_num}) > table:nth-child(2) > tbody > tr > td.bb-splitsTable__data.bb-splitsTable__data--text > a')
    if not a:
        return None
    return {
        '選手名': a.get_text(),
        'link': f"https://{BASE_DOMAIN_NAME}{a.get('href')}",
    }


def get_pitcher_past_record(player):
    html = download_html(player['link'])
    soup = BeautifulSoup(html, 'html.parser')
    player['防御率'] = soup.select_one(
        '#js-tabDom01 > section:nth-child(1) > table > tbody > tr:nth-child(2) > td:nth-child(1)').get_text()
    player['勝数'] = soup.select_one(
        '#js-tabDom01 > section:nth-child(1) > table > tbody > tr:nth-child(2) > td:nth-child(8)').get_text()
    player['敗数'] = soup.select_one(
        '#js-tabDom01 > section:nth-child(1) > table > tbody > tr:nth-child(2) > td:nth-child(9)').get_text()
    player['勝敗'] = f"{player['勝数']}-{player['敗数']}"
    rows = soup.select(f'#game_p > tbody > tr')
    past_records = []
    for row in rows:
        past_record = {
            '日付': row.select_one(f'td:nth-child(1) > a').get_text(),
            '対戦チーム': row.select_one(f'td:nth-child(2)').get_text(),
            '登板': row.select_one(f'td:nth-child(3)').get_text(),
            '結果': row.select_one(f'td:nth-child(4)').get_text(),
            '投球回': row.select_one(f'td:nth-child(5)').getText(),
            '投球数': row.select_one(f'td:nth-child(6)').getText(),
            '打者': row.select_one(f'td:nth-child(7)').getText(),
            '被安打': row.select_one(f'td:nth-child(8)').getText(),
            '被本塁打': row.select_one(f'td:nth-child(9)').getText(),
            '奪三振': row.select_one(f'td:nth-child(10)').getText(),
            '与四球': row.select_one(f'td:nth-child(11)').getText(),
            '与死球': row.select_one(f'td:nth-child(12)').getText(),
            '暴投': row.select_one(f'td:nth-child(13)').getText(),
            'ボーク': row.select_one(f'td:nth-child(14)').getText(),
            '失点': row.select_one(f'td:nth-child(15)').getText(),
            '自責点': row.select_one(f'td:nth-child(16)').getText(),
        }
        past_records.append(past_record)
    勝数 = sum([1 for r in past_records if r['結果'] == '勝'])
    敗数 = sum([1 for r in past_records if r['結果'] == '敗'])
    投球回 = sum([float(r['投球回']) for r in past_records])
    自責点 = sum([int(r['自責点']) for r in past_records])
    if 投球回 <= 0:
        return {
            '調子': -1,
            'icon': ':question:',
            '防御率': '-',
            '勝敗': '-',
        }
    防御率 = 自責点 * 9 / 投球回
    condition = get_pitcher_condition(防御率)
    return {
        '調子': condition,
        'icon': get_condition_icon(condition),
        '防御率': f"{防御率:.2f}",
        '勝敗': f"{勝数}-{敗数}",
    }


def get_players(html, team_num):
    soup = BeautifulSoup(html, 'html.parser')
    rows = soup.select(f'#strt_mem > section > div > section:nth-child({team_num}) > table:nth-child(3) > tbody > tr')
    players = []
    if not rows:
        return players
    for row in rows:
        player = {
            '打順': row.select_one(f'td:nth-child(1)').get_text(),
            '位置': row.select_one(f'td:nth-child(2)').get_text(),
            '選手名': row.select_one(f'td:nth-child(3) > a').get_text(),
            '打': row.select_one(f'td:nth-child(4)').get_text(),
            '打率': row.select_one(f'td:nth-child(5)').getText(),
            'link': f"https://{BASE_DOMAIN_NAME}{row.select_one(f'td:nth-child(3) > a').get('href')}",
        }
        players.append(player)
    return players


def get_past_record(player):
    html = download_html(player['link'])
    soup = BeautifulSoup(html, 'html.parser')
    header_title = soup.select_one('#js-tabDom01 > section:nth-child(1) > header > h2').get_text().strip()
    if header_title == '打者成績':
        player['本塁打'] = soup.select_one(
            '#js-tabDom01 > section:nth-child(1) > table > tbody > tr:nth-child(2) > td:nth-child(8)').get_text()
    else:
        player['本塁打'] = soup.select_one(
            '#js-tabDom01 > section:nth-child(2) > table > tbody > tr:nth-child(2) > td:nth-child(8)').get_text()
    rows = soup.select(f'#game_b > tbody > tr')
    past_records = []
    for row in rows:
        past_record = {
            '日付': row.select_one(f'td:nth-child(1) > a').get_text(),
            '対戦チーム': row.select_one(f'td:nth-child(2)').get_text(),
            '打数': row.select_one(f'td:nth-child(3)').get_text(),
            '安打': row.select_one(f'td:nth-child(4)').get_text(),
            '本塁打': row.select_one(f'td:nth-child(5)').getText(),
            '打点': row.select_one(f'td:nth-child(6)').getText(),
            '得点': row.select_one(f'td:nth-child(7)').getText(),
            '三振': row.select_one(f'td:nth-child(8)').getText(),
            '四球': row.select_one(f'td:nth-child(9)').getText(),
            '死球': row.select_one(f'td:nth-child(10)').getText(),
            '打席結果': row.select_one(f'td:nth-child(11)').getText(),
        }
        past_records.append(past_record)
    打数 = sum([int(r['打数']) for r in past_records])
    if 打数 <= 0:
        return {
            '調子': -1,
            'icon': ':hatena_spin:',
            '打率': '-',
            '本塁打': '-',
        }
    past_rate = sum([int(r['安打']) for r in past_records]) / 打数
    condition = get_condition(past_rate)
    if 打数 < 6:
        icon = ':hatena_spin:'
    else:
        icon = get_condition_icon(condition)
    return {
        '調子': condition,
        'icon': icon,
        '打率': "1.000" if past_rate == 1 else f"{past_rate:.3f}"[1:],
        '本塁打': sum([int(r['本塁打']) for r in past_records]),
    }


def get_condition(rate):
    if rate >= 0.400:
        return 1  # 絶好調
    elif rate >= 0.300:
        return 2  # 好調
    elif rate >= 0.200:
        return 3  # 普通
    elif rate >= 0.100:
        return 4  # 不調
    elif rate >= 0.001:
        return 5  # 絶不調
    else:
        return 6


def get_pitcher_condition(rate):
    if rate < 2.50:
        return 1  # 絶好調
    elif rate < 3.50:
        return 2  # 好調
    elif rate < 4.50:
        return 3  # 普通
    elif rate < 5.50:
        return 4  # 不調
    elif rate < 6.50:
        return 5  # 絶不調
    else:
        return 6


def get_condition_icon(condition):
    if condition == 0:
        return ":duck_exciting_yukawashiichi:"
    else:
        return f":condition{condition}:"


def create_message(game, team_a, team_b):
    messages = []
    pitcher_a = team_a['pitcher']
    pitcher_b = team_b['pitcher']
    players_a = team_a['batters']
    players_b = team_b['batters']
    if players_a and players_b:
        messages.append(f"*{game['team_name_a']} (直近６試合)*")
        # messages.append('')
        messages.append(get_pitcher_header())
        messages.append(get_label_from_pitcher(pitcher_a))
        messages.append(get_header())
        for p in players_a:
            messages.append(get_label_from_player(p))
        messages.append('')
        messages.append(f"*{game['team_name_b']} (直近６試合)*")
        # messages.append('')
        messages.append(get_pitcher_header())
        messages.append(get_label_from_pitcher(pitcher_b))
        messages.append(get_header())
        for p in players_b:
            messages.append(get_label_from_player(p))
        messages.append('')
        return '\n'.join(messages)


def get_header():
    tab = '\t'
    return f"打)  選手名{tab}打率(今期){tab}本塁打(今期)"


def get_label_from_player(p):
    tab = '\t'
    return f"{p['打順']}{tab}{p['直近']['icon']} <{p['link']}|{p['選手名']}>{tab}{p['直近']['打率']} ({p['打率']}){tab}{p['直近']['本塁打']} ({p['本塁打']})"


def get_pitcher_header():
    tab = '\t'
    return f"投)  選手名{tab}防御率(今期){tab}勝敗(今期)"


def get_label_from_pitcher(p):
    tab = '\t'
    return f"{p['直近']['icon']} <{p['link']}|{p['選手名']}>{tab}{p['直近']['防御率']} ({p['防御率']}){tab}{p['直近']['勝敗']} ({p['勝敗']})"


def create_title(game):
    return f"*:baseball: {game['title']}*\n*{game['team_name_a']} vs {game['team_name_b']}*\n*<{game['link']}|{game['status']}>*"


if __name__ == '__main__':
    lambda_handler(None, None)

from pydantic.dataclasses import dataclass
from typing import List
from classes.player import Player
from classes.pitcher_recent_stats import PitcherRecentStats


@dataclass
class Pitcher(Player):
    RecentStats: List[PitcherRecentStats] = None
    link: str = ''
    選手名: str = ''
    防御率: float = 0.0
    登板: int = 0
    先発: int = 0
    完投: int = 0
    完封: int = 0
    無四球: int = 0
    交代完了: int = 0
    勝利: int = 0
    敗戦: int = 0
    ホールド: int = 0
    HP: int = 0
    セーブ: int = 0
    勝率: float = 0.0
    投球回: float = 0.0
    打者: int = 0
    被安打: int = 0
    被本塁打: int = 0
    奪三振: int = 0
    奪三振率: float = 0.0
    与四球: int = 0
    与死球: int = 0
    暴投: int = 0
    ボーク: int = 0
    失点: int = 0
    自責点: int = 0
    QS率: float = 0.0
    被打率: float = 0.0
    K_BB: float = 0.0
    WHIP: float = 0.0

    @property
    def 勝敗(self) -> str:
        return f'{self.勝利}-{self.敗戦}'

    @property
    def 直近_投球回(self) -> float:
        return sum([float(r.投球回) for r in self.RecentStats])

    @property
    def 直近_勝利(self) -> int:
        return sum([1 for r in self.RecentStats if r.結果 == '勝'])

    @property
    def 直近_敗戦(self) -> int:
        return sum([1 for r in self.RecentStats if r.結果 == '敗'])

    @property
    def 直近_勝敗(self) -> str:
        return f'{self.直近_勝利}-{self.直近_敗戦}'

    @property
    def 直近_投球回(self) -> float:
        return sum([r.投球回 for r in self.RecentStats])

    @property
    def 直近_自責点(self) -> int:
        return sum([r.自責点 for r in self.RecentStats])

    @property
    def 直近_防御率(self) -> float:
        if self.直近_投球回 == 0:
            return -1
        return float(f'{self.直近_自責点 * 9 / self.直近_投球回:.2f}')

    @property
    def 直近_調子(self) -> float:
        if self.直近_投球回 == 0:
            return -1
        rate = float(self.直近_防御率)
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

    @property
    def icon(self):
        if self.直近_調子 == -1:
            return ":hatena_spin:"
        elif self.直近_調子 == 0:
            return ":duck_exciting_yukawashiichi:"
        else:
            return f":condition{self.直近_調子}:"

    @property
    def label(self):
        tab = '\t'
        if self.直近_投球回 == 0:
            return f"{self.icon} <{self.link}|{self.選手名}>{tab}- ({self.防御率}){tab}- ({self.勝敗})"
        else:
            return f"{self.icon} <{self.link}|{self.選手名}>{tab}{self.直近_防御率} ({self.防御率}){tab}{self.直近_勝敗} ({self.勝敗})"

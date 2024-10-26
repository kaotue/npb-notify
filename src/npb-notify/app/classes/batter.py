from pydantic.dataclasses import dataclass
from typing import List
from classes.player import Player
from classes.batter_recent_stats import BatterRecentStats


@dataclass
class Batter(Player):
    link: str
    選手名: str
    打順: int
    位置: str
    打: str
    打率: float = 0.0
    RecentStats: List[BatterRecentStats] = None
    試合: int = 0
    打席: int = 0
    打数: int = 0
    安打: int = 0
    二塁打: int = 0
    三塁打: int = 0
    本塁打: int = 0
    塁打: int = 0
    打点: int = 0
    得点: int = 0
    三振: int = 0
    四球: int = 0
    死球: int = 0
    犠打: int = 0
    犠飛: int = 0
    盗塁: int = 0
    盗塁死: int = 0
    併殺打: int = 0
    出塁率: float = 0.0
    長打率: float = 0.0
    OPS: float = 0.0
    得点圏: float = 0.0
    失策: int = 0

    @property
    def 直近_打数(self) -> int:
        return sum([r.打数 for r in self.RecentStats])

    @property
    def 直近_打率(self) -> float:
        return sum([r.安打 for r in self.RecentStats]) / sum([r.打数 for r in self.RecentStats])

    @property
    def 直近_本塁打(self) -> int:
        return sum([r.本塁打 for r in self.RecentStats])

    @property
    def 直近_打率_label(self) -> str:
        return "1.000" if self.直近_打率 == 1 else f"{self.直近_打率:.3f}"[1:]

    @property
    def 打率_label(self) -> str:
        if self.打率 == 1:
            return "1.000"
        elif self.打率 > 0:
            return f"{self.打率:.3f}"[1:]
        else:
            return '-'

    @property
    def 直近_調子(self) -> int:
        rate = self.直近_打率
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

    @property
    def icon(self):
        if self.直近_成績不十分:
            return ":hatena_spin:"
        elif self.直近_調子 == 0:
            return ":duck_exciting_yukawashiichi:"
        else:
            return f":condition{self.直近_調子}:"

    @property
    def 直近_成績不十分(self) -> bool:
        return self.直近_打数 < 6

    @property
    def label(self):
        tab = '\t'
        if self.直近_打数 == 0:
            return f"{self.打順}{tab}{self.icon} <{self.link}|{self.選手名}>{tab}- ({self.打率_label}){tab}- ({self.本塁打})"
        else:
            return f"{self.打順}{tab}{self.icon} <{self.link}|{self.選手名}>{tab}{self.直近_打率_label} ({self.打率_label}){tab}{self.直近_本塁打} ({self.本塁打})"

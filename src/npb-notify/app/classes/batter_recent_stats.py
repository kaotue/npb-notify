from pydantic.dataclasses import dataclass
from datetime import date


@dataclass
class BatterRecentStats:
    日付: date
    対戦チーム: str = ''
    打数: int = 0
    安打: int = 0
    本塁打: int = 0
    打点: int = 0
    得点: int = 0
    三振: int = 0
    四球: int = 0
    死球: int = 0
    打席結果: str = ''


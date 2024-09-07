from pydantic.dataclasses import dataclass
from datetime import date


@dataclass
class PitcherRecentStats:
    日付: date
    対戦チーム: str = ''
    登板: str = ''
    結果: str = ''
    投球回: float = 0.0
    投球数: int = 0
    打者: int = 0
    被安打: int = 0
    被本塁打: int = 0
    奪三振: int = 0
    与四球: int = 0
    与死球: int = 0
    暴投: int = 0
    ボーク: int = 0
    失点: int = 0
    自責点: int = 0

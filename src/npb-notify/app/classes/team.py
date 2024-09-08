from pydantic.dataclasses import dataclass
from typing import List, Optional
from classes.pitcher import Pitcher
from classes.batter import Batter


@dataclass
class Team:
    name: str
    pitcher: Optional[Pitcher] = None
    batters: Optional[List[Batter]] = None

    @property
    def label(self) -> List[str]:
        tab = '\t'
        messages = []
        messages.append(f"*{self.name} (直近６試合)*")
        messages.append(f"投)  選手名{tab}防御率(今期){tab}勝敗(今期)")
        messages.append(self.pitcher.label)
        messages.append(f"打)  選手名{tab}打率(今期){tab}本塁打(今期)")
        for b in self.batters:
            messages.append(b.label)
        return messages

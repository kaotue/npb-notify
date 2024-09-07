from pydantic.dataclasses import dataclass
from classes.team import Team


@dataclass
class Game:
    title: str
    link: str
    home_team: Team
    away_team: Team
    date: str
    status: str
    stadium: str
    home_score: int
    away_score: int

    def get_notify_header(self):
        return f'*:baseball: {self.title}*\n*{self.home_team.name} vs {self.away_team.name}*\n*<{self.link}|{self.status}>*'

    def get_notify_message(self):
        messages = []
        messages.extend(self.home_team.label)
        messages.append('')
        messages.extend(self.away_team.label)
        messages.append('')
        return '\n'.join(messages)

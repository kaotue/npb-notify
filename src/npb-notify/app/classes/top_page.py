from pydantic.dataclasses import dataclass


@dataclass
class TopPage:
    game_page_url: str
    game_status: str

from pydantic.dataclasses import dataclass


@dataclass
class NpbContext:
    top_url: str
    color: str

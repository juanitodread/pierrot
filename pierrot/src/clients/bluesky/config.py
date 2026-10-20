from dataclasses import dataclass


@dataclass
class BlueskyConfig:
    username: str
    password: str
    use_mock: bool = True

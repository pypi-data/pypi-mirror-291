import sys
from collections import UserDict
from typing import Any, ClassVar, overload
import httpx
from bs4 import BeautifulSoup
from . import Player


if sys.version_info >= (3, 12):
    from typing import Self
else:
    from typing_extensions import Self


class Players(UserDict):

    BASE_URL: ClassVar[str] = "http://baseballsavant.mlb.com/"
    MLB_SEARCH: ClassVar[str] = BASE_URL + "statcast_search"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.data: dict[int, Player]
        self._by_slug: dict[str, Player] = {}
        super().__init__(self, *args, **kwargs)

    def fetch(self) -> Self:
        home: httpx.Response = httpx.get(self.MLB_SEARCH, follow_redirects=True)
        home.raise_for_status()
        return self._parse_bs4(BeautifulSoup(home.content, "html.parser"))

    def _parse_bs4(self, soup: BeautifulSoup) -> Self:
        for player in soup.find_all("option"):
            try:
                self.add(
                    Player(
                        id=player.attrs["value"],
                        fullname=player.text.strip().split("\n")[-1].strip(),
                    )
                )
            except (KeyError, ValueError):
                continue
        return self

    def add(self, player: Player) -> Self:
        self.data[player.id] = player
        self._by_slug[player.slug] = player
        return self

    @overload
    def __getitem__(self, key: int) -> Player: ...

    @overload
    def __getitem__(self, key: str) -> list[Player]: ...

    def __getitem__(self, key: int | str) -> Player | list[Player]:
        if isinstance(key, int):
            return super().__getitem__(key)
        return [player for slug, player in self._by_slug.items() if key.lower() in slug]

    def __getattr__(self, key: str) -> list[Player]:
        return self.__getitem__(key)

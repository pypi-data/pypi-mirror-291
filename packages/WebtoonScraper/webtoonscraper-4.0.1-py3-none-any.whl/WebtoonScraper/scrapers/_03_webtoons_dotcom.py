"""Download Webtoons from `webtoons.com/en`."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from furl import furl

from ..exceptions import InvalidURLError, InvalidWebtoonIdError
from ._01_scraper import Scraper, reload_manager


class WebtoonsDotcomScraper(Scraper[int]):
    """Scrape webtoons from Webtoon Originals."""

    BASE_URL = "https://www.webtoons.com/en/action/jungle-juice"
    TEST_WEBTOON_ID = 5291  # Wumpus
    TEST_WEBTOON_IDS = (
        5291,  # Wumpus
        263735,  # Spook
    )
    PLATFORM = "webtoons_dotcom"
    base_url: str | None = None

    def __init__(self, webtoon_id, /) -> None:
        super().__init__(webtoon_id)
        self.headers.update(Referer="http://www.webtoons.com")

    @reload_manager
    def fetch_webtoon_information(self, *, reload: bool = False) -> None:
        if self.base_url:
            response = self.hxoptions.get(f"{self.base_url}/list?title_no={self.webtoon_id}")
        else:
            self.base_url = "https://www.webtoons.com/en/action/jungle-juice"
            self.is_original = True
            response = self.hxoptions.get(f"{self.base_url}/list?title_no={self.webtoon_id}")

            if response.status_code == 404:
                self.base_url = "https://www.webtoons.com/en/challenge/meme-girls"
                self.is_original = False
                response = self.hxoptions.get(f"{self.base_url}/list?title_no={self.webtoon_id}")

        if response.status_code == 404:
            del self.is_original
            raise InvalidWebtoonIdError.from_webtoon_id(self.webtoon_id, type(self), rating_notice=True)

        title = response.soup_select_one('meta[property="og:title"]', no_empty_result=True).get("content")
        assert isinstance(title, str)

        webtoon_thumbnail = response.soup_select_one('meta[property="og:image"]', no_empty_result=True).get("content")
        assert isinstance(
            webtoon_thumbnail, str
        ), f"""Cannot get webtoon thumbnail. "og:image": {response.soup_select_one('meta[property="og:image"]')}"""

        self.title = title
        self.webtoon_thumbnail_url = webtoon_thumbnail

    @reload_manager
    def fetch_episode_information(self, *, reload: bool = False) -> None:
        # getting title_no
        url = f"{self.base_url}/list?title_no={self.webtoon_id}"
        title_no_str = (
            self.hxoptions.get(url).soup_select_one("#_listUl > li", no_empty_result=True).get("data-episode-no")
        )
        assert isinstance(title_no_str, str)
        title_no = int(title_no_str)

        # getting list of titles
        selector = "#_bottomEpisodeList > div.episode_cont > ul > li"
        url = f"{self.base_url}/prologue/viewer?title_no={self.webtoon_id}&episode_no={title_no}"
        selected = self.hxoptions.get(url).soup_select(selector)

        subtitles = []
        episode_ids = []
        for element in selected:
            episode_no_str = element["data-episode-no"]
            assert isinstance(episode_no_str, str)
            episode_no = int(episode_no_str)
            subtitles.append(element.select_one("span.subj").text)  # type: ignore
            episode_ids.append(episode_no)

        self.episode_titles = subtitles
        self.episode_ids = episode_ids

    def get_episode_image_urls(self, episode_no) -> list[str]:
        episode_id = self.episode_ids[episode_no]
        url = f"{self.base_url}/prologue/viewer?title_no={self.webtoon_id}&episode_no={episode_id}"
        episode_images_url = self.hxoptions.get(url).soup_select("#_imageList > img")
        episode_image_urls = [element["data-url"] for element in episode_images_url]
        if TYPE_CHECKING:
            episode_image_urls = [
                episode_image_url for episode_image_url in episode_image_urls if isinstance(episode_image_url, str)
            ]
        return episode_image_urls

    @classmethod
    def from_url(
        cls,
        url,
        *args,  # cookie나 bearer같은 optional parameter를 잡기 위해 필요.
        **kwargs,
    ):
        """Raw URL에서 자동으로 웹툰 ID를 추출합니다."""
        # 마음에 안 드는 코드이지만 뭐 달리 방법이 없음
        furl_ = furl(url)
        try:
            webtoon_id, matched = cls._extract_webtoon_id(furl_)
        except Exception as e:
            raise InvalidURLError.from_url(url, cls) from e

        if webtoon_id is None or matched is None:
            raise InvalidURLError.from_url(url, cls)

        self = cls(webtoon_id, *args, **kwargs)
        self.base_url = f"https://{furl_.host}/{str(furl_.path).removesuffix('/').removesuffix('/list')}"
        self.is_original = matched["genre"] != "canvas"

        return self

    @classmethod
    def _extract_webtoon_id(cls, url) -> tuple[int | None, re.Match[str] | None]:
        if url.host != "www.webtoons.com":
            return None, None
        matched = re.match(r"/(?P<language_code>[a-zA-Z_-]+)/(?P<genre>[a-zA-Z_-]+)/(?P<seo_id>[a-zA-Z_-]+)/list", str(url.path))
        if not matched:
            return None, None
        webtoon_id_str = url.query.params.get("title_no")
        if not webtoon_id_str:
            return None, None
        return int(webtoon_id_str), matched

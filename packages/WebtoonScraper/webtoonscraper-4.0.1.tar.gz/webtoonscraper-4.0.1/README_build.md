**Check latest version [here](https://github.com/ilotoki0804/WebtoonScraper).**
# WebtoonScraper

[![GitHub Downloads (all assets, latest release)](https://img.shields.io/github/downloads/ilotoki0804/WebtoonScraper/latest/total?label=executable%20downloads)](https://github.com/ilotoki0804/WebtoonScraper/releases)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/WebtoonScraper)](https://pypi.org/project/WebtoonScraper/)
[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Filotoki0804%2FWebtoonScraper&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://github.com/ilotoki0804/WebtoonScraper)
[![Sponsoring](https://img.shields.io/badge/Sponsoring-PayPal-blue?logo=GitHub%20Sponsors&logoColor=white)](https://paypal.me/ilotoki0804)

저작권과 책임에 대한 내용을 더욱 자세히 알고 싶다면 [이 문서](docs/copyright.md)를 참고해 주세요.

* [WebtoonScraper](#webtoonscraper)
    * [How to use](#how-to-use)
    * [Installation](#installation)

## How to use

대부분의 웹툰은 다음과 같이 터미널에 `webtoon download`를 치고 큰따옴표로 감싼 URL을 뒤에 위치하면 작동합니다.

```console
webtoon download "https://comic.naver.com/webtoon/list?titleId=819217"
```

**일부 웹툰 플랫폼의 경우에는 추가적인 정보가 반드시 필요한 경우가 있습니다. 반드시 [플랫폼별 다운로드 가이드](docs/platforms.md)를 참고해 주세요.**

## Installation

파이썬(3.10 이상, 최신 버전 권장)을 설치하고 터미널에서 다음과 같은 명령어를 실행합니다.

```console
pip install -U WebtoonScraper[full]
```

업데이트시에도 똑같은 코드를 이용할 수 있습니다.

잘 설치되었는지를 확인하려면 다음의 명령어로 테스트해 보세요.

```console
webtoon --version
```

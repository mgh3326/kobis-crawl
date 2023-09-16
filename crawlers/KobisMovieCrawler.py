import requests
from bs4 import BeautifulSoup

from lxml import etree


class KobisMovieCrawler:
    KOBIS_URL = "https://www.kobis.or.kr"
    KOBIS_MOVIE_DETAIL_URL = f"{KOBIS_URL}/kobis/mobile/mast/mvie/searchMovieDtl.do"

    def __init__(self, movie_code):
        self.movie_code = movie_code

    def run(self):
        response = self._get_response_from_page()
        if response:
            return self._extract_thumbnail_url(response)
        print(f"Failed to get response for movie_code = {self.movie_code}")
        return None

    def _get_response_from_page(self):
        params = {
            "movieCd": self.movie_code,
        }
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection": "keep-alive",
            "Cookie": "ACEUCI=1; ACEFCID=UID-65005669C9930A3E1577C2E3; AUFAB2A31560820885=1694520937686727822|2|1694520937686727822|1|1694520937544627822; _ga=GA1.3.505816218.1694520938; AUAB2A31560820885=1694520937714177520%7C2%7C1694520937686727822%7C1%7C1694520937544627822%7C1; ARAB2A31560820885=httpswwwkobisorkrkobisbusinessstatoffcsearchOfficHitTotListdohttpswwwkobisorkrkobisbusinessstatoffcsearchOfficHitTotListdo; ASAB2A31560820885=1694520937714177520%7C1694522956383484053%7C1694520937714177520%7C0%7Chttpswwwgooglecom; JSESSIONID=HjcWlC0LnYJH9R71Q0k11kL0bL1clGbNXNRpmgY2WQ6yYGQC3ltf{UNICODE_CHARACTER}1712779882{UNICODE_CHARACTER}174661068; ACEUACS=1694692521737907857; AUAZ3A54623=1694692521147179796%7C2%7C1694692521147179796%7C1%7C1694692521737Z7UO1; ARAZ3A54623=httpswwwkobisorkrkobismobilemastmviesearchMovieDtldomovieCd20239574httpswwwgooglecom; _gid=GA1.3.971478028.1694692522; _ga_62TRNDZ0CK=GS1.3.1694692522.2.0.1694692522.0.0.0; ASAZ3A54623=1694692521147179796%7C1694692549932372176%7C1694692521147179796%7C0%7Chttpswwwgooglecom",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Whale/3.22.205.18 Safari/537.36",
            "sec-ch-ua": '"Whale";v="3", "Not-A.Brand";v="8", "Chromium";v="116"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
        }
        try:
            response = requests.get(
                self.KOBIS_MOVIE_DETAIL_URL, params=params, headers=headers
            )
        except requests.RequestException as e:
            print("Exception occurred while making a request to the API: ", e)
            return None
        return response

    @staticmethod
    def _extract_thumbnail_url(response):
        if response.status_code != 200:
            return {"thumbnail_url": None}
        soup = BeautifulSoup(response.text, "html.parser")
        dom = etree.HTML(str(soup))
        movie_href = dom.xpath('//*[@id="contents"]/div/div[1]/a/@href')
        if movie_href:
            image_url = f"{KobisMovieCrawler.KOBIS_URL}/{movie_href[0]}"
            return {"thumbnail_url": image_url}
        return {"thumbnail_url": None}

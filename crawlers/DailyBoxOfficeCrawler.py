import json

import requests
from dotenv import load_dotenv
import os


class DailyBoxOfficeCrawler:
    load_dotenv()
    API_KEY = os.getenv("KOBIS_API_KEY")
    BOX_OFFICE_BASE_URL = f"http://kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?key={API_KEY}"

    VALID_Y_N_VALUES = ["Y", "N", None]
    VALID_K_F_VALUES = ["K", "F", None]

    def __init__(self, targetDt, multiMovieYn=None, repNationCd=None):
        self.validate_values(multiMovieYn, repNationCd)
        self.targetDt = targetDt
        self.multiMovieYn = multiMovieYn
        self.repNationCd = repNationCd

    def run(self):
        response = self._get_response_from_api()
        if response is not None and response.status_code == 200:
            data = json.loads(response.text)
            box_office_results = data["boxOfficeResult"]["dailyBoxOfficeList"]
            return box_office_results

    def validate_values(self, multi_movie_yn, rep_nation_cd):
        valid_y_n_values = ["Y", "N", None]
        valid_k_f_values = ["K", "F", None]

        if (
            multi_movie_yn not in valid_y_n_values
            or rep_nation_cd not in valid_k_f_values
        ):
            raise ValueError(
                'multi_movie_yn must be "Y", "N", or None and rep_nation_cd must be "K", "F", or None'
            )

    def _get_response_from_api(self):
        params = {
            "targetDt": self.targetDt,
            "multiMovieYn": self.multiMovieYn,
            "repNationCd": self.repNationCd,
        }
        try:
            response = requests.get(
                DailyBoxOfficeCrawler.BOX_OFFICE_BASE_URL, params=params
            )
        except requests.RequestException as e:
            print("Exception occurred while making a request to the API: ", e)
            return None
        return response

import os
from dotenv import load_dotenv
from models.DailyBoxOffice import DailyBoxOffice


class Kobis:
    load_dotenv()
    API_KEY = os.getenv("KOBIS_API_KEY")
    BOX_OFFICE_BASE_URL = f"http://kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?key={API_KEY}"

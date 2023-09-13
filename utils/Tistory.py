import os
from dotenv import load_dotenv


class Tistory:
    load_dotenv()
    API_KEY = os.getenv("TISTORY_API_KEY")
    SECRET_KEY = os.getenv("TISTORY_SECRET_KEY")

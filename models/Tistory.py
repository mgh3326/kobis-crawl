import os

import requests
from dotenv import load_dotenv
import json


class Tistory:
    load_dotenv()
    APP_ID = os.getenv("TISTORY_APP_ID")
    SECRET_KEY = os.getenv("TISTORY_SECRET_KEY")
    TISTORY_CODE = os.getenv("TISTORY_CODE")
    TISTORY_REDIRECT_URI = os.getenv("TISTORY_REDIRECT_URI")
    TISTORY_STATE = os.getenv("TISTORY_STATE")
    TISTORY_ACCESS_TOKEN = os.getenv("TISTORY_ACCESS_TOKEN")

    @staticmethod
    def authorize():
        response = requests.get(
            f"https://www.tistory.com/oauth/authorize?client_id={Tistory.APP_ID}&response_type=code&state={Tistory.TISTORY_STATE}&redirect_uri={Tistory.TISTORY_REDIRECT_URI}"
        )
        print(response.text)

    @staticmethod
    def access_token():
        response = requests.get(
            f"https://www.tistory.com/oauth/access_token?client_id={Tistory.APP_ID}&client_secret={Tistory.SECRET_KEY}&grant_type=authorization_code&redirect_uri={Tistory.TISTORY_REDIRECT_URI}&code={Tistory.TISTORY_CODE}"
        )
        return response.text.replace("access_token=", "")

    @staticmethod
    def blog_info():
        response = requests.get(
            f"https://www.tistory.com/apis/blog/info?access_token={Tistory.TISTORY_ACCESS_TOKEN}&output=json"
        )
        print(response.text)

    @staticmethod
    def category_list(blogName):
        response = requests.get(
            f"https://www.tistory.com/apis/category/list?access_token={Tistory.TISTORY_ACCESS_TOKEN}&output=json&blogName={blogName}"
        )
        json.loads(response.text)
        print(response.text)

    @staticmethod
    def post_write(blog_name, category_id, title, content, tag, slogan, visibility=3):
        data = {
            "category": category_id,
            "title": title,
            "content": content,
            "tag": tag,
            "slogan": slogan,
            "visibility": visibility,
        }
        response = requests.post(
            f"https://www.tistory.com/apis/post/write?access_token={Tistory.TISTORY_ACCESS_TOKEN}&output=json&blogName={blog_name}",
            data=data,
        )
        json.loads(response.text)
        print(response.text)

    @staticmethod
    def post_attach(blog_name, file):
        response = requests.post(
            f"https://www.tistory.com/apis/post/attach?access_token={Tistory.TISTORY_ACCESS_TOKEN}&output=json&blogName={blog_name}",
            files={"uploadedfile": file},
        )
        if response.status_code == 200:
            response_data = json.loads(response.text)
            print(response.text)
            if response_data["tistory"]["status"] == "200":
                return response_data["tistory"]["url"]
            else:
                return None
        else:
            print(response.text)

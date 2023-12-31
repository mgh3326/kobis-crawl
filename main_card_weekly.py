import datetime
import io

import requests
from PIL import Image
from jinja2 import (
    Environment,
    FileSystemLoader,
)

from models.Kobis import Kobis
from models.KobisMovie import KobisMovie
from models.Tistory import Tistory


def post_daily_box_office_card(date, multiMovieYn=None, repNationCd=None):
    date_str = date.strftime("%Y%m%d")
    show_range = "20230908~20230910"
    show_range_str = "2023년 9월 8일~9월 10일"
    e = Environment(loader=FileSystemLoader("templates/"))
    daily_box_office_list = Kobis.daily_box_office_crawl(
        date_str, multiMovieYn, repNationCd
    )
    template = e.get_template("daily_box_office_card.html")
    movies = []
    for obj in daily_box_office_list:
        kobis_movie = KobisMovie(obj.movieCd)
        kobis_movie.crawl()
        image_url = kobis_movie.thumbnail_url
        obj_to_dict = obj.to_dict()
        if image_url is not None:
            im = Image.open(requests.get(image_url, stream=True).raw)
            buffer = io.BytesIO()
            im = im.convert("RGB")
            im.save(buffer, format="JPEG", quality=100)
            val = buffer.getvalue()
            uploaded_tistory_url = Tistory.post_attach("mgh3326", val)
            obj_to_dict["thumbnail_url"] = uploaded_tistory_url
        else:
            obj_to_dict["thumbnail_url"] = None
        movies.append(obj_to_dict)
    content = template.render(movies=movies, date=show_range_str)
    category_id = "1141907"
    if multiMovieYn == "Y":
        multi_movie_type = "다양성"
    elif multiMovieYn == "N":
        multi_movie_type = "상업"
    else:
        multi_movie_type = None
    if repNationCd == "K":
        nation_movie_type = "한국"
    elif repNationCd == "F":
        nation_movie_type = "외국"
    else:
        nation_movie_type = None
    title = f"{show_range_str} 주말 영화 순위(박스오피스)"
    if multi_movie_type is None and nation_movie_type is None:
        title += f"- ({'전체'})"
    elif nation_movie_type is None:
        title += f"- ({multi_movie_type} 영화)"
    elif multi_movie_type is None:
        title += f"- ({nation_movie_type} 영화)"
    else:
        title += f"- ({nation_movie_type} {multi_movie_type} 영화)"
    slogan = f"{date_str}_box_office_{multiMovieYn}_{repNationCd}"
    titles = [obj.title() for obj in daily_box_office_list]
    Tistory.post_write(
        "mgh3326",
        category_id,
        title,
        content,
        f"박스 오피스,박스오피스, 영화 순위, 영화, {show_range_str} 주말 영화 순위," + ",".join(titles),
        slogan,
        0,
    )


target_date = datetime.datetime.strptime("20230910", "%Y%m%d").date()
post_daily_box_office_card(target_date)
post_daily_box_office_card(target_date, None, "K")
post_daily_box_office_card(target_date, None, "F")
post_daily_box_office_card(target_date, "Y")
post_daily_box_office_card(target_date, "Y", "K")
post_daily_box_office_card(target_date, "Y", "F")
post_daily_box_office_card(target_date, "N")
post_daily_box_office_card(target_date, "N", "K")
post_daily_box_office_card(target_date, "N", "F")

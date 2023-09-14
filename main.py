import datetime

from jinja2 import (
    Environment,
    FileSystemLoader,
)

from models.Kobis import Kobis
from models.Tistory import Tistory


def post_daily_box_office(date, multiMovieYn=None, repNationCd=None):
    date_str = date.strftime("%Y%m%d")
    e = Environment(loader=FileSystemLoader("templates/"))
    daily_box_office_list = Kobis.daily_box_office_crawl(
        date_str, multiMovieYn, repNationCd
    )
    template = e.get_template("daily_box_office.html")
    movies = [obj.to_dict() for obj in daily_box_office_list]  # 각 객체를 딕셔너리로 변환
    content = template.render(movies=movies, date=date.strftime("%Y년 %m월 %d일"))
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
    title = f"{date.strftime('%Y년 %m월 %d일')} 일간 영화 순위(박스오피스)"
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
        f"박스 오피스,박스오피스, 영화 순위, 영화, {date.strftime('%Y년 %m월 %d일')} 영화 순위,"
        + ",".join(titles),
        slogan,
    )


# Kobis.crawl("20230911")
# Kobis.crawl("20230911", "Y")
# Kobis.crawl("20230911", "Y", "K")
# Kobis.crawl("20230911", "Y", "F")
# Kobis.crawl("20230911", "N")
# Kobis.crawl("20230911", "N", "K")
# Kobis.crawl("20230911", "N", "F")

# access_token = Tistory.authorize()
# access_token = Tistory.access_token()
# Tistory.blog_info()
# Tistory.category_list("mgh3326")
current_date = datetime.date.today()
yesterday_date = current_date - datetime.timedelta(days=1)
post_daily_box_office(yesterday_date)
post_daily_box_office(yesterday_date, None, "K")
post_daily_box_office(yesterday_date, None, "F")
post_daily_box_office(yesterday_date, "Y")
post_daily_box_office(yesterday_date, "Y", "K")
post_daily_box_office(yesterday_date, "Y", "F")
post_daily_box_office(yesterday_date, "N")
post_daily_box_office(yesterday_date, "N", "K")
post_daily_box_office(yesterday_date, "N", "F")

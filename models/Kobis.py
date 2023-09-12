from models.DailyBoxOffice import DailyBoxOffice


class Kobis:
    @staticmethod
    def daily_box_office_crawl(targetDt, multiMovieYn=None, repNationCd=None):
        return DailyBoxOffice.crawl(targetDt, multiMovieYn, repNationCd)

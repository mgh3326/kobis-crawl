from crawlers.DailyBoxOfficeCrawler import DailyBoxOfficeCrawler


class DailyBoxOffice:
    def __init__(
        self,
        rnum,
        rank,
        rankInten,
        rankOldAndNew,
        movieCd,
        movieNm,
        openDt,
        salesAmt,
        salesShare,
        salesInten,
        salesChange,
        salesAcc,
        audiCnt,
        audiInten,
        audiChange,
        audiAcc,
        scrnCnt,
        showCnt,
    ):
        self.rnum = rnum
        self.rank = rank
        self.rankInten = rankInten
        self.rankOldAndNew = rankOldAndNew
        self.movieCd = movieCd
        self.movieNm = movieNm
        self.openDt = openDt
        self.salesAmt = salesAmt
        self.salesShare = salesShare
        self.salesInten = salesInten
        self.salesChange = salesChange
        self.salesAcc = salesAcc
        self.audiCnt = audiCnt
        self.audiInten = audiInten
        self.audiChange = audiChange
        self.audiAcc = audiAcc
        self.scrnCnt = scrnCnt
        self.showCnt = showCnt

    @staticmethod
    def crawl(targetDt, multiMovieYn, repNationCd):
        box_office_results = DailyBoxOfficeCrawler(
            targetDt, multiMovieYn, repNationCd
        ).run()
        daily_box_office_list = [
            DailyBoxOffice(**box_office_data) for box_office_data in box_office_results
        ]
        return daily_box_office_list

    def title(self):
        return self.movieNm

    def movie_code(self):
        return self.movieCd

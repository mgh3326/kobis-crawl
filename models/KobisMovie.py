from crawlers.KobisMovieCrawler import KobisMovieCrawler


class KobisMovie:
    def __init__(self, movieCd):
        self.movieCd = movieCd
        self.thumbnail_url = None

    def crawl(self):
        movie_info = KobisMovieCrawler(self.movieCd).run()
        self.thumbnail_url = movie_info["thumbnail_url"]
        return movie_info

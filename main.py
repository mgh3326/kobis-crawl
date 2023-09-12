from models.Kobis import Kobis

# Kobis.crawl("20230911")
# Kobis.crawl("20230911", "Y")
# Kobis.crawl("20230911", "Y", "K")
# Kobis.crawl("20230911", "Y", "F")
# Kobis.crawl("20230911", "N")
# Kobis.crawl("20230911", "N", "K")
# Kobis.crawl("20230911", "N", "F")
daily_box_office_list = Kobis.daily_box_office_crawl("20230911")
print(f"Crawled {len(daily_box_office_list)} models")
for daily_box_office in daily_box_office_list:
    print(daily_box_office.title())

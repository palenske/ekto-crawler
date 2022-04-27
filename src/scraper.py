import requests
from time import sleep
import random
from parsel import Selector
from utils.pkl_manager import Pkl_Manager

# https://ektoplazm.com/
class Scraper:
    def __init__(self, url) -> None:
        self.BASE_URL = url
        self.STYLE_BASE_URL = f"{self.BASE_URL}style/"

    def fetch(self, url):
        time_list = [5, 4, 2, 3]
        proxies = {
            "https": "200.116.164.252:8080",
            "http": "103.149.162.195:80",
            "http": "101.33.70.103:80",
        }
        try:
            sleep(random.choice(time_list))
            response = requests.get(url, timeout=5)
        except requests.Timeout:
            return None
        else:
            if response.status_code != 200:
                return None
            return response.text

    def get_categories(self, html_content):
        selector = Selector(text=html_content)
        return selector.css("#sidemenu > div:nth-child(2) > a::text").getall()

    def get_bpm_media(self, list_bpm):
        try:
            return round((sum(list(map(int, list_bpm))) / len(list_bpm)))
        except ZeroDivisionError:
            return None

    def get_album_data(self, html_content, post):
        selector = Selector(text=html_content)

        return dict(
            title=selector.css(f"#{post} > h1 > a::text").get(),
            styles=selector.css(f"#{post} span.style > strong > a::text").getall(),
            download_count=selector.css(
                f"#{post} div > p > span > span.dc > strong::text"
            ).get(),
            comments_count=selector.css(f"#{post} p.postmetadata > a::text").re_first(
                r"\d+"
            ),
            url=selector.css(f"#{post} h1 > a::attr(href)").get(),
            img=selector.css(f"#{post} > div > a > img::attr(src)").get(),
            tracks=selector.css(f"#{post} > div > div > span.t::text").getall(),
            media_bpm=self.get_bpm_media(
                selector.css(f"#{post} > div > div > span.d::text").re(r"\d+")
            ),
        )

    def get_all_albums(self, html_content):
        selector = Selector(text=html_content)
        posts_list_id = selector.css(".post::attr(id)").getall()
        return [self.get_album_data(html_content, post_id) for post_id in posts_list_id]

    def scrape_posts_style(self, style):
        url = f"{self.STYLE_BASE_URL}{style}"
        html_content = self.fetch(url)
        selector = Selector(text=html_content)
        max_pages = selector.css(".navigation span.pages::text").re(r"\d+")[1]
        url_list = [f"{url}/page/{n}" for n in range(2, int(max_pages) + 1)]
        random.shuffle(url_list)

        albums_data = self.get_all_albums(html_content)
        for url in url_list:
            new_html_content = self.fetch(url)
            albums_data.extend(self.get_all_albums(new_html_content))

        Pkl_Manager.write_file(albums_data, f"src/data/by_category/{style}.pkl")

        return albums_data


scrape = Scraper("https://ektoplazm.com/")

print(scrape.scrape_posts_style("techtrance"))

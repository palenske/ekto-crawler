import requests
from time import sleep
from parsel import Selector


class Scraper:
    def __init__(self) -> None:
        pass

    def fetch(self, url):
        try:
            sleep(1)
            response = requests.get(url, timeout=3)
        except requests.Timeout:
            return None
        else:
            if response.status_code != 200:
                return None
            return response.text

    def get_categories(self, html_content):
        selector = Selector(text=html_content)
        return selector.css("#sidemenu > div:nth-child(2) > a::text").getall()

    def scrape_posts_style(self, style):
        self.max_pages = 0
        BASE_URL = f"https://ektoplazm.com/style/{style}"

        def get_album_data(url):
            html_content = self.fetch(url)
            selector = Selector(text=html_content)
            self.max_pages = selector.css(".navigation span.pages::text").re(r"\d+")[1]
            posts_list_id = selector.css(".post::attr(id)").getall()
            return [
                dict(
                    title=selector.css(f"#{post} > h1 > a::text").get(),
                    styles=selector.css(
                        f"#{post} span.style > strong > a::text"
                    ).getall(),
                    download_count=selector.css(
                        f"#{post} div > p > span > span.dc > strong::text"
                    ).get(),
                    comments_count=selector.css(
                        f"#{post} p.postmetadata > a::text"
                    ).re_first(r"\d+"),
                    url=selector.css(f"#{post} h1 > a::attr(href)").get(),
                )
                for post in posts_list_id
            ]

        album_data = get_album_data(BASE_URL)

        url_list = [f"{BASE_URL}/page/{n}" for n in range(2, int(self.max_pages) + 1)]

        [album_data.extend(get_album_data(url)) for url in url_list]

        return album_data


scrape = Scraper()

print(scrape.scrape_posts_style("psy-dub"))

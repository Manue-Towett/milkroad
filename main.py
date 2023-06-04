import os
import json
import base64
import threading
from queue import Queue

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from utils import Logger
import utils.useful_paths as up

class MRScraper:
    """Scrapes articles from https://milkroad.com/news/"""
    def __init__(self) -> None:
        self.logger = Logger(__class__.__name__)
        self.logger.info("*****Milkroad Scraper Started*****")

        self.root_url = "https://milkroad.com/news/"
        self.api_url = "https://brain.bitfo.com/api/milkroad/news"

        self.end_page_reached = False
        self.articles, self.crawled, self.crawled_images = [], [], []

        self.queue = Queue()

    def __init_query(self) -> str:
        """Makes a initial request to the site"""
        try:
            self.logger.info("Making INIT_QUERY to milkroad...")

            response = requests.get(self.root_url, proxies=up.PROXIES, 
                                    verify=up.VERIFY)
            
            soup = BeautifulSoup(response.text, "html.parser")
            script = soup.find("script", {"id":"__NEXT_DATA__"}) 

            json_data = json.loads(script.string)
            data = json_data["props"]["pageProps"]["data"]["news"]

            [self.articles.append(item["slug"]) for item in data]

            return data[-1]["published_at"]
        
        except:
            self.logger.error("Fatal: INIT_QUERY failed!")
    
    def __get_next_page(self, pub_date: str) -> str:
        """Get articles from the next page
        
           Arg:
             - pub_date: the date in which the last article in the current
                         page was published
           Return:
             - the publication date of the last article in the results 
               returned from the next page
        """
        self.logger.info("Fetching articles from next page...")

        encoded_date = base64.b64encode(pub_date.encode()).decode()

        params = {"cursor": encoded_date, "limit" : 30}

        try:
            response = requests.get(self.api_url, proxies=up.PROXIES, 
                                    verify=up.VERIFY, params=params)
            
            json_data = json.loads(response.content)["items"]

            if len(json_data):
                [self.articles.append(item["slug"]) for item in json_data]
                
                return json_data[-1]["published_at"]
            else:
                self.end_page_reached = True

        except:
            self.logger.error("Fatal: could not find next page results!")
    
    def __fetch_article(self, url_slug: str) -> None:
        """Fetches an article from milkroad and saves its html
        
           Arg:
             - url_slug: the relative url to the article to be fetched
        """
        if not os.path.exists("./milkroad/"):
            os.makedirs("./milkroad/")

        try:
            response = requests.get(self.root_url + url_slug,
                                    proxies=up.PROXIES, verify=up.VERIFY)
            
            soup = BeautifulSoup(response.text, "html.parser")

            try:
                section = soup.find("section", {"id":"post"})
            except:
                section = soup.find("section", {"id":"page"})

            self.__download_images(section)
                    
            with open(f"./milkroad/{url_slug}.html", "w", encoding="utf-8") as file:
                file.write(up.CONTAINER % {"content": section})
            
            self.crawled.append(url_slug)

            queue = len(self.articles) - len(self.crawled)

            self.logger.info(f"Queue: {queue} | Crawled: {len(self.crawled)}")

        except:
            self.logger.warn(f"Couldn't fetch article {self.root_url}{url_slug}")
    
    def __download_images(self, soup: BeautifulSoup) -> None:
        """Downloads images found in the current article
        
           Arg:
             - soup: BeautifulSoup object of the article
        """
        if not os.path.exists("./images/"):
            os.makedirs("./images/")

        images = []

        for image_tag in soup.select("img"):
            image_url = image_tag["src"].split("?")[0]

            if image_url.startswith("http") and not image_url in self.crawled_images:
                images.append(image_url)
        
        [self.__fetch_image(url) for url in images if not url in self.crawled_images]
        
        self.logger.info("Images downloaded: {}".format(len(self.crawled_images)))
    
    def __fetch_image(self, image_url: str) -> None:
        """Fetches an image with a given url
        
           Arg:
             - image_url: the url to the given image to be downloaded
        """
        for _ in range(3):
            if image_url in self.crawled_images:
                break

            try:
                headers = {"user-agent": UserAgent().chrome.strip()}

                response = requests.get(image_url, stream=True, headers=headers)

                file_id = image_url.split("/")[-1]

                if file_id.endswith("png") or file_id.endswith("jpg") \
                    or file_id.endswith("jpeg") or file_id.endswith("gif"):
                    file_name = file_id
                else:
                    file_name = f"{file_id}.png"

                with open(f"./images/{file_name}", "wb") as file:
                    file.write(response.content)
                
                self.crawled_images.append(image_url)
                
                break

            except:pass
    
    def __create_thread_work(self) -> None:
        """Creates work to be done by threads"""
        [self.queue.put(article) for article in self.articles]
        self.queue.join()
    
    def __work(self) -> None:
        """Work to be done by threads"""
        while True:
            article_slug = self.queue.get()

            self.__fetch_article(article_slug)

            self.queue.task_done()
    
    def scrape(self) -> None:
        """Entry point to the scraper"""
        end_article_date = self.__init_query()

        while not self.end_page_reached:
            self.logger.info("Queue: {}".format(len(self.articles)))

            end_article_date = self.__get_next_page(end_article_date)
        
        [threading.Thread(target=self.__work, daemon=True).start() for _ in range(20)]

        self.logger.info("Total articles: %s | "
                         "Scraping content..." % len(self.articles))

        self.__create_thread_work()

if __name__ == "__main__":
    scraper = MRScraper()
    scraper.scrape()
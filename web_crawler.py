"""Module to crawl websites"""

from __future__ import annotations

import os
import time
import traceback
from collections import deque

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

from configs import Configs
from utils import Utils


class WebCrawler:
    """WebCrawler Module"""

    def __init__(self):
        self.queue = deque()
        self.visited = set()
        self.utils = Utils()


    def dump_data(self):
        pass


    def load_data(self):
        pass


    def update_urls(self, page_source):
        soup = BeautifulSoup(page_source, 'html.parser')
        soup = soup.find(Configs.TOP_ELEMENT, id=Configs.CONTENT_COMMON_ID)
        if not soup:
            return None

        img_tags = soup.find_all('img')
        for img_tag in img_tags:
            image_url = None
            if img_tag.get('src'):
                url = self.utils.preprocess_image_url(img_tag.get('src'))
                image_path = self.utils.download_image(url)
                if image_path:
                    image_path = "app\\" + image_path
                img_tag['src'] = image_path
            elif img_tag.get('data-src'):
                url = self.utils.preprocess_image_url(img_tag.get('data-src'))
                image_path = self.utils.download_image(url)
                if image_path:
                    image_path = "app\\" + image_path
                img_tag['data-src'] = image_path

        link_tags = soup.find_all('a')
        for link_tag in link_tags:
            if link_tag.get('href'):
                link_tag['href'] = self.utils.preprocess_web_url(link_tag.get('href'))

        return str(soup)


    def crawl_website(self):
        """Crawls entire website one url at a time and saves
        theit content in doc files in DATA_DIR.
        """
        self.queue.append(Configs.PAGE_URL)
        while len(self.queue):
            web_url = self.queue.popleft()

            if web_url in self.visited:
                continue

            page_source, links = self.crawl_url(web_url)
            if not page_source:
                continue
            html = self.update_urls(page_source)
            if html:
                markdown = self.utils.html_to_markdown(html)
                self.utils.write_text_file(markdown, web_url)


            self.visited.add(web_url)
            for link in links:
                if link not in self.visited and link.startswith("https://docs.aryaka.com"):
                    self.queue.append(link)


        return None


    def crawl_url(self, url):
        """_summary_

        Args:
            url (str): the url that needs to be crawled

        Returns:
            webElements or None: page source of url
        """
        page_source, links = None, []
        try:
            options = webdriver.FirefoxOptions()
            options.add_argument("-headless")
            driver = webdriver.Firefox(options=options)
            driver.get(url)
            wait = WebDriverWait(driver, Configs.MAX_WAITING_TIME)
            wait.until(EC.visibility_of_all_elements_located((By.ID, Configs.PAGE_COMMON_ID)))
            time.sleep(5)

            page_source = driver.page_source
            links = [
                self.utils.preprocess_web_url(anchor.get_attribute('href')) 
                for anchor in driver.find_elements(by=By.TAG_NAME, value="a") 
                if anchor.get_attribute('href') is not None
            ]
        except Exception as ex:
            print(traceback.print_exc())
            print(url)
            return page_source, links
        finally:
            driver.close()

        return page_source, links
    

if __name__ == '__main__':
    crawler = WebCrawler()
    crawler.crawl_website()

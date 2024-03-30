'''The utils Module'''

from __future__ import annotations

import os
import re

import requests
import html2text

from configs import Configs

class Utils:
    """Module to store utility functions for WebCrawler"""

    def __init__(self):
        pass


    def write_text_file(self, content, url):
        file_path = self.get_file_path(url)
        with open(file_path, 'wb') as f:
            f.write(content.encode())


    def download_image(self, image_url):
        image_name = image_url.split('/')[-1]
        if not os.path.exists(Configs.IMAGE_DIR):
            os.mkdir(Configs.IMAGE_DIR)
        image_path = os.path.join(Configs.IMAGE_DIR, image_name)
        try:
            data = requests.get(image_url).content
            with open(image_path, 'w') as f:
                f.write(data) 
            return image_path
        except Exception as e:
            print(e, image_url)
            return None
        
    
    def html_to_markdown(self, html):
        converter = html2text.HTML2Text()
        converter.ignore_links = False
        return converter.handle(html)


    def get_file_path(self, page_url):
        page_url = page_url[8:]
        if not os.path.exists(Configs.DATA_DIR):
            os.mkdir(Configs.DATA_DIR)
        return os.path.join(Configs.DATA_DIR, '-'.join(page_url.split('/')) + '.txt')


    def preprocess_image_url(self, url):
        if not url.startswith(('http://', 'https://')):
            url = Configs.BASE_URL + url
        regex = r'(\S*\.png|\S*\.jpg)\S*'
        try:
            matches = re.findall(regex, url)
            return matches[0]
        except IndexError as e:
            print(e, url)
            return url


    def preprocess_web_url(self, url):
        if not url.startswith(('http://', 'https://')):
            url = Configs.BASE_URL + url
        regex = r'(\S*\d+)\S*'
        try:
            matches = re.findall(regex, url)
            return matches[0]
        except IndexError as e:
            print(e, 'url:', url)
            return url


if __name__ == '__main__':
    utils = Utils()
    utils.preprocess_image_url('https://docs/aryaka.com/download/attachments/1542430/UntticketingIcon.png?version=1&modificationDate=1711559163535&cacheVersion=1&api=v2')
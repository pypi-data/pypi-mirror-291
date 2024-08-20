import requests
from bs4 import BeautifulSoup


class WebCrawler:
    def __init__(self, url):
        self.url = url

    def fetch_content(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup.get_text()
        else:
            raise Exception(f"Failed to fetch {self.url} (Status code: {response.status_code})")
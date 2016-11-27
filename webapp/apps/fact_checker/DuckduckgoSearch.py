import requests
import re
from bs4 import BeautifulSoup



class DuckduckgoSearch:
    def __init__(self, search):
        self.search = search.replace(" ", "+")
        self.request = "https://duckduckgo.com/html/?q=" + self.search
        result = requests.get(self.request)
        self.parsed_html = BeautifulSoup(result.text, 'html.parser')

    def get_link_list(self):
        link_list = self.parsed_html.body.find_all('a', attrs={'class': 'result__url'})

        final_website_list = []
        for link in link_list:
            if link.get('href'):
                final_website_list.append(link.get('href'))

        return final_website_list
        # return final_website_list,request,click_bait

    def get_request(self):
        return self.request

    def estimate_number_click_bait(self):
        title_list = self.parsed_html.body.find_all('a', attrs={'class': 'result__a'})
        click_bait = 0
        for a in title_list:
            res = re.search(" \d?\d?\d ", a.text)
            if res:
                click_bait += 1

        return click_bait



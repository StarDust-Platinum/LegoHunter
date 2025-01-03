from os.path import dirname, basename, isfile, join
import glob

import time
import requests
from selenium import webdriver


modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]


class Site:
    def __init__(self, filter_blacklist):
        self.blacklist = filter_blacklist.split(',')

    def url2html(self, url, method="requests"):
        if method == "requests":
            headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
            try:
                req = requests.get(url, headers=headers)
                html = req.text
            except requests.exceptions.RequestException:
                return
            return html
        elif method == "selenium":
            browser = webdriver.Remote(
                command_executor = "http://selenium:4444/wd/hub",
                options = webdriver.ChromeOptions()
            )

            browser.get(url)
            time.sleep(5)
            html = browser.page_source
            browser.quit()
            return html
        return

    def determine_item(self, title, set_number):
        if (set_number not in title):
            return False
        for word in self.blacklist:
            if (word in title):
                return False
        return True
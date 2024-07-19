import time
import requests
from selenium import webdriver


def url2html(url, method="requests"):
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

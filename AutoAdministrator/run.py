import requests

url = "http://nginx/item/crawl-cron"
try:
    requests.get(url)
except:
    pass

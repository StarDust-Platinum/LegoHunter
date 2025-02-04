import requests, json

url = "http://nginx/item/crawl-cron"
with open("config.json", 'r') as file:
    config = json.load(file)
try:
    requests.post(url, json=config)
except:
    pass

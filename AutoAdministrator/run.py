import requests

url = "http://legohunter:5000/crawl"
try:
    requests.get(url)
except:
    pass
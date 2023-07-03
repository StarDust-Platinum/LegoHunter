import time
import requests
from bs4 import BeautifulSoup

def crawl_set(set_id, headers):
    try:
        req = requests.get("https://www.brickeconomy.com/search?query={}".format(set_id), headers=headers)
    except requests.exceptions.RequestException:
        return None
    bs = BeautifulSoup(req.text, "html.parser")
    try:
        table = bs.find(id="ContentPlaceHolder1_ctlSetsOverview_GridViewSets")
        if table.find("td", {"class":{"ctlsets-left"}}).div.get_text()[:5] == set_id:    
            name = table.find("h4").get_text()[6:]
            theme = table.find("small", string="Theme").parent.get_text()[6:]
            year = table.find("small", string="Year").parent.get_text()[5:]
            pieces = int("".join(table.find("small", string="Pieces").parent.get_text()[7:].split(",")))
            availability = table.find("small", string="Availability").parent.get_text()[13:]
            retail = float(table.find("small", string="Retail").parent.get_text()[8:])
            if availability == "Retired":
                value = float(table.find("small", string="Value").parent.get_text()[7:])
            else:
                value = retail
    except AttributeError:
        return None
    lego_set_row = {
        "set_id": set_id,
        "name": name,
        "theme": theme,
        "year": year,
        "pieces": pieces,
        "availability": availability,
        "retail": retail,
        "value": value
    }
    return lego_set_row

def crawl_item_from_paypay(set_id, headers):
    lego_item_rows = []
    uncrawled_page = True
    try:
        req = requests.get("https://paypayfleamarket.yahoo.co.jp/search/LEGO%20{}?conditions=NEW&open=1".format(set_id), headers=headers)
    except requests.exceptions.RequestException:
        return None
    bs = BeautifulSoup(req.text, "html.parser")
    try:
        while uncrawled_page:
            for itm in bs.find(id="itm").find_all("a"):
                title = itm.find("img")["alt"]
                if "互換" in title:
                    continue
                price = int("".join(itm.find("p").get_text()[:-1].split(",")))
                url = "https://paypayfleamarket.yahoo.co.jp" + itm["href"]
                lego_item_row = {
                    "set_id": set_id,
                    "title": title,
                    "price": price,
                    "url": url,
                }
                lego_item_rows.append(lego_item_row)
            last_li = bs.find("ul", class_="sc-2300bd7f-1 kTZkbX").find_all("li")[-1]
            if last_li.get_text()==" 次へ ":
                time.sleep(10)
                req = requests.get("https://paypayfleamarket.yahoo.co.jp"+last_li.find("a")["href"], headers=headers)
                bs = BeautifulSoup(req.text, "html.parser")
            else:
                uncrawled_page = False
    except AttributeError:
        return None
    return lego_item_rows
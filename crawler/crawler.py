import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
#from selenium.webdriver.common.by import By
#from selenium.webdriver import ActionChains

def crawl_set(set_id):
    options = Options()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.brickeconomy.com/search?query={}".format(set_id))
    time.sleep(1)
    bs = BeautifulSoup(driver.page_source, "html.parser")
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

def crawl_item_from_mercari(set_id):
    lego_item_rows = []
    uncrawled_page = True
    options = Options()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    driver.get("https://jp.mercari.com/search?keyword=LEGO%20{}&item_condition_id=1&status=on_sale".format(set_id))
    time.sleep(1)
    bs = BeautifulSoup(driver.page_source, "html.parser")
    try:
        while uncrawled_page:
            for itm in bs.find_all("a", class_="sc-295d2608-2 cyhDfc"):
                title = itm.find("div", class_="imageContainer__f8ddf3a2")["aria-label"][:-6]
                if "互換" in title:
                    continue
                price = int("".join(itm.find("span", class_="number__6b270ca7").get_text().split(",")))
                url = "https://jp.mercari.com" + itm["href"]
                lego_item_row = {
                    "set_id": set_id,
                    "title": title,
                    "price": price,
                    "url": url,
                }
                lego_item_rows.append(lego_item_row)
            button = True
            if button:
                #driver.find_element(By.CSS_SELECTOR, ".merButton.secondary__01a6ef84.medium__01a6ef84")
                #ActionChains(driver).click(button).perform()
                uncrawled_page = False
            else:
                uncrawled_page = False
    except AttributeError:
        return None
    driver.close()
    return lego_item_rows

def crawl_item_from_paypay(set_id):
    lego_item_rows = []
    uncrawled_page = True
    options = Options()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    driver.get("https://paypayfleamarket.yahoo.co.jp/search/LEGO%20{}?conditions=NEW&open=1".format(set_id))
    time.sleep(1)
    bs = BeautifulSoup(driver.page_source, "html.parser")
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
                driver.get("https://paypayfleamarket.yahoo.co.jp"+last_li.find("a")["href"])
                print("https://paypayfleamarket.yahoo.co.jp"+last_li.find("a")["href"])
                time.sleep(1)
                bs = BeautifulSoup(driver.page_source, "html.parser")
            else:
                uncrawled_page = False
    except AttributeError:
        return None
    return lego_item_rows

def crawl_item_from_rakuma(set_id):
    #disallowed in robots.txt
    lego_item_rows = []
    uncrawled_page = True
    options = Options()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    driver.get("https://fril.jp/s?query=lego%20{}&status=new&transaction=selling".format(set_id))
    time.sleep(1)
    bs = BeautifulSoup(driver.page_source, "html.parser")
    try:
        while uncrawled_page:
            for itm in bs.find_all("div", class_="item-box"):
                title = itm.find("a", class_="link_search_title").find("span").get_text()
                if "互換" in title:
                    continue
                price = int("".join(itm.find("p", class_="item-box__item-price").find_all("span")[1].get_text().split(",")))
                url = itm.find("a", class_="link_search_title")["href"]
                lego_item_row = {
                    "set_id": set_id,
                    "title": title,
                    "price": price,
                    "url": url,
                }
                lego_item_rows.append(lego_item_row)

            next_exist = True
            if next_exist:
                uncrawled_page = False
            else:
                uncrawled_page = False
    except AttributeError:
        return None
    driver.close()
    return lego_item_rows

def crawl_item_from_yafuoku(set_id):
    #disallowed in robots.txt
    lego_item_rows = []
    uncrawled_page = True
    options = Options()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    driver.get("https://auctions.yahoo.co.jp/search/search?p=lego+{}&va=lego+{}&istatus=1&is_postage_mode=1&dest_pref_code=13&exflg=1&b=1&n=50".format(set_id,set_id))
    time.sleep(1)
    bs = BeautifulSoup(driver.page_source, "html.parser")
    try:
        while uncrawled_page:
            for itm in bs.find_all("li", class_="Product"):
                title = itm.find("a", class_="Product__titleLink js-rapid-override js-browseHistory-add").get_text()
                if "互換" in title:
                    continue
                price = int("".join(itm.find("span", class_="Product__priceValue u-textRed").get_text()[:-1].split(",")))
                url = itm.find("a", class_="Product__titleLink js-rapid-override js-browseHistory-add")["href"]
                lego_item_row = {
                    "set_id": set_id,
                    "title": title,
                    "price": price,
                    "url": url,
                }
                lego_item_rows.append(lego_item_row)
            
            next_exist = True
            if next_exist:
                uncrawled_page = False
            else:
                uncrawled_page = False
    except AttributeError:
        return None
    return lego_item_rows

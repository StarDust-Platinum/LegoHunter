import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
#from selenium.webdriver.common.by import By
#from selenium.webdriver import ActionChains


def get_html(url, method="requests"):
    if method == "requests":
        headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
        try:
            req = requests.get(url, headers=headers)
            html = req.text
        except requests.exceptions.RequestException:
            return None
        return html
    elif method == "selenium":
        options = Options()
        options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        time.sleep(1)
        html = driver.page_source
        driver.quit()
        return html


def crawl_set(set_id):
    row = {}
    try:
        bs = BeautifulSoup(get_html("https://www.brickeconomy.com/search?query={}".format(set_id)), "html.parser")
        table = bs.find(id="ContentPlaceHolder1_ctlSetsOverview_GridViewSets")
        if table.find("td", {"class":{"ctlsets-left"}}).div.get_text()[:5] == set_id:    
            try:
                row["name"] = table.find("h4").get_text()[6:]
            except:
                pass
            try:
                row["theme"] = table.find("small", string="Theme").parent.get_text()[6:]
            except:
                pass
            try:
                row["year"] = table.find("small", string="Year").parent.get_text()[5:]
            except:
                pass
            try:
                row["pieces"] = int("".join(table.find("small", string="Pieces").parent.get_text()[7:].split(",")))
            except:
                pass
            try:
                row["availability"] = table.find("small", string="Availability").parent.get_text()[13:]
            except:
                pass
            try:
                row["retail"] = float(table.find("small", string="Retail").parent.get_text()[8:])
            except:
                pass
            try:
                row["value"] = float(table.find("small", string="Value").parent.get_text()[7:])
            except:
                pass
    except AttributeError:     
        return None
    return row


def crawl_amazonjp(set_id):
    rows = []
    is_uncrawled = True
    try:
        bs = BeautifulSoup(get_html(r"https://www.amazon.co.jp/s?k=lego+{}&__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&crid=2IGP4U26DZPY4&sprefix=lego+{}%2Caps%2C151&ref=nb_sb_noss_1".format(set_id, set_id)), "html.parser")
        while is_uncrawled:
            for itm in bs.find_all("div", class_="sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20"):
                row = {"site": "amazonjp"}
                try:
                    row["title"] = itm.find("span", class_="a-size-base-plus a-color-base a-text-normal").get_text()
                    if (set_id not in row["title"]) or ("互換" in row["title"]) or ("LED" in row["title"]):
                        continue
                except:
                    continue
                try:
                    row["price"] = int("".join(itm.find("span", class_="a-offscreen").get_text()[1:].split(",")))
                except:
                    pass
                try:
                    row["rating_number"] = int("".join(itm.find("span", class_="a-size-base s-underline-text").get_text().split(",")))
                except:
                    pass
                try:
                    row["url"] = "https://www.amazon.co.jp" + itm.find("a", class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal")["href"]
                except:
                    pass
                rows.append(row)
            is_uncrawled = False
    except AttributeError:
        return None
    return rows


def crawl_rakuten(set_id):
    rows = []
    is_uncrawled = True
    try:
        bs = BeautifulSoup(get_html(r"https://search.rakuten.co.jp/search/mall/lego+{}/".format(set_id)), "html.parser")
        while is_uncrawled:
            for itm in bs.find_all("div", class_="dui-card searchresultitem"):
                row = {"site": "rakuten"}
                try:
                    row["title"] = itm.find("h2", class_="title-link-wrapper--2sUFJ title-link-wrapper-grid--db8v2").get_text()
                    if (set_id not in row["title"]) or ("互換" in row["title"]) or ("LED" in row["title"]) or ("中古" in row["title"]):
                        continue
                except:
                    continue
                try:
                    row["price"] = int("".join(itm.find("div", class_="price--OX_YW").get_text()[:-1].split(",")))
                except:
                    pass
                try:
                    row["rating_number"] = int("".join(itm.find("span", class_="legend").get_text()[1:-2].split(",")))
                except:
                    pass
                try:
                    row["url"] = itm.find("h2", class_="title-link-wrapper--2sUFJ title-link-wrapper-grid--db8v2").find("a")["href"]
                except:
                    pass
                rows.append(row)
            is_uncrawled = False
    except AttributeError:
        return None
    return rows


def crawl_mercari(set_id):
    rows = []
    is_uncrawled = True
    try:
        bs = BeautifulSoup(get_html("https://jp.mercari.com/search?keyword=LEGO%20{}&item_condition_id=1&status=on_sale".format(set_id), "selenium"), "html.parser")
        while is_uncrawled:
            for itm in bs.find_all("a", class_="sc-f9b0f7ab-2 gfwMYx"):
                row = {"site": "mercari"}
                try:
                    row["title"] = itm.find("div", class_="imageContainer__f8ddf3a2")["aria-label"][:-6]
                    if (set_id not in row["title"]) or ("互換" in row["title"]) or ("LED" in row["title"]):
                        continue
                except:
                    continue
                try:
                    row["price"] = int("".join(itm.find("span", class_="number__6b270ca7").get_text().split(",")))
                except:
                    pass
                try:
                    row["url"] = "https://jp.mercari.com" + itm["href"]
                except:
                    url = None
                rows.append(row)
            is_uncrawled = False
    except AttributeError:
        return None
    return rows


def crawl_paypayfurima(set_id):
    rows = []
    is_uncrawled = True
    try:
        bs = BeautifulSoup(get_html("https://paypayfleamarket.yahoo.co.jp/search/LEGO%20{}?conditions=NEW&open=1".format(set_id)), "html.parser")
        while is_uncrawled:
            for itm in bs.find(id="itm").find_all("a"):
                row = {"site": "paypayfurima"}
                try:
                    row["title"] = itm.find("img")["alt"]
                    if (set_id not in row["title"]) or ("互換" in row["title"]) or ("LED" in row["title"]):
                        continue
                except:
                    continue
                try:
                    row["price"] = int("".join(itm.find("p").get_text()[:-1].split(",")))
                except:
                    pass
                try:
                    row["url"] = "https://paypayfleamarket.yahoo.co.jp" + itm["href"]
                except:
                    pass
                rows.append(row)
            
            last_li = bs.find("ul", class_="sc-2300bd7f-1 kTZkbX").find_all("li")[-1]
            if last_li.get_text()==" 次へ ":
                time.sleep(5)
                bs = BeautifulSoup(get_html("https://paypayfleamarket.yahoo.co.jp"+last_li.find("a")["href"]), "html.parser")
            else:
                is_uncrawled = False
    except AttributeError:
        return None
    return rows


def crawl_rakuma(set_id):
    #disallowed in robots.txt
    rows = []
    is_uncrawled = True
    try:
        bs = BeautifulSoup(get_html("https://fril.jp/s?query=lego%20{}&status=new&transaction=selling".format(set_id)), "html.parser")
        while is_uncrawled:
            for itm in bs.find_all("div", class_="item-box"):
                row = {"site": "rakuma"}
                try:
                    row["title"] = itm.find("a", class_="link_search_title").find("span").get_text()
                    if (set_id not in row["title"]) or ("互換" in row["title"]) or ("LED" in row["title"]):
                        continue
                except:
                    continue
                try:
                    row["price"] = int("".join(itm.find("p", class_="item-box__item-price").find_all("span")[1].get_text().split(",")))
                except:
                    pass
                try:
                    row["url"] = itm.find("a", class_="link_search_title")["href"]
                except:
                    pass
                rows.append(row)
            is_uncrawled = False
    except AttributeError:
        return None
    return rows


def crawl_yafuoku(set_id):
    #disallowed in robots.txt
    rows = []
    is_uncrawled = True
    try:
        bs = BeautifulSoup(get_html("https://auctions.yahoo.co.jp/search/search?p=lego+{}&va=lego+{}&istatus=1&is_postage_mode=1&dest_pref_code=13&exflg=1&b=1&n=50".format(set_id,set_id)), "html.parser")
        while is_uncrawled:
            for itm in bs.find_all("li", class_="Product"):
                row = {"site": "yafuoku"}
                try:
                    row["title"] = itm.find("a", class_="Product__titleLink js-rapid-override js-browseHistory-add").get_text()
                    if (set_id not in row["title"]) or ("互換" in row["title"]) or ("LED" in row["title"]):
                        continue
                except:
                    continue
                try:
                    row["price"] = int("".join(itm.find("span", class_="Product__priceValue u-textRed").get_text()[:-1].split(",")))
                except:
                    pass
                try:
                    row["url"] = itm.find("a", class_="Product__titleLink js-rapid-override js-browseHistory-add")["href"]
                except:
                    pass
                rows.append(row)
            is_uncrawled = False
    except AttributeError:
        return None
    return rows

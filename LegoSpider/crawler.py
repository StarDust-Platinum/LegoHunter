import time
from datetime import datetime
from bs4 import BeautifulSoup
from webtoolbox import url2html


def judge_item(title, set_number):
    wordblacklist = ["互換", "LED", "ケース"]

    if (set_number not in title):
        return False

    for word in wordblacklist:
        if (word in title):
            return False

    return True


def crawl_amazonjp(set_number):
    records = []
    page_unprocessed = True
    try:
        html = url2html(r"https://www.amazon.co.jp/s?k=lego+{}&__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&crid=2IGP4U26DZPY4&sprefix=lego+{}%2Caps%2C151&ref=nb_sb_noss_1".format(set_number, set_number))
        bs = BeautifulSoup(html, "html.parser")
        while page_unprocessed:
            for itm in bs.find_all("div", class_="sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20"):
                record = {"set_number":"'{}'".format(set_number), "site":"'amazonjp'"}
                try:
                    record["title"] = "'{}'".format(itm.find("span", class_="a-size-base-plus a-color-base a-text-normal").get_text().replace("'", "_"))
                    if not judge_item(record["title"], set_number):
                        continue
                    record["price"] = "'{}'".format("".join(itm.find("span", class_="a-offscreen").get_text()[1:].split(",")))
                    record["url"] = "'{}'".format("https://www.amazon.co.jp" + itm.find("a", class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal")["href"])
                    record["date_modified"] = "'{}'".format(datetime.now())
                except:
                    continue
                records.append(record)

            next_page = False
            if next_page:
                pass
            else:
                page_unprocessed = False

    except AttributeError:
        return None
    return records


def crawl_rakuten(set_number):
    records = []
    page_unprocessed = True
    try:
        html = url2html(r"https://search.rakuten.co.jp/search/mall/lego+{}/".format(set_number))
        bs = BeautifulSoup(html, "html.parser")
        while page_unprocessed:
            for itm in bs.find_all("div", class_="dui-card searchresultitem overlay-control-wrapper--2W6PV title-control-wrapper--1YBX9"):
                record = {"set_number":"'{}'".format(set_number), "site":"'rakuten'"}
                try:
                    record["title"] = "'{}'".format(itm.find("h2", class_="title-link-wrapper--2sUFJ title-link-wrapper-grid--db8v2").get_text().replace("'", "_"))
                    if not judge_item(record["title"], set_number):
                        continue
                    record["price"] = "'{}'".format("".join(itm.find("div", class_="price--OX_YW").get_text()[:-1].split(",")))
                    record["url"] = "'{}'".format(itm.find("h2", class_="title-link-wrapper--2sUFJ title-link-wrapper-grid--db8v2").find("a")["href"])
                    record["date_modified"] = "'{}'".format(datetime.now())
                except:
                    continue
                records.append(record)

            next_page = False
            if next_page:
                pass
            else:
                page_unprocessed = False

    except AttributeError:
        return None
    return records


def crawl_mercari(set_number):
    records = []
    page_unprocessed = True
    try:
        html = url2html("https://jp.mercari.com/search?keyword=LEGO%20{}&item_condition_id=1&status=on_sale".format(set_number), "selenium")
        bs = BeautifulSoup(html, "html.parser")
        while page_unprocessed:
            for itm in bs.find_all("li", class_="sc-bcd1c877-2 cvAXgx"):
                record = {"set_number":"'{}'".format(set_number), "site":"'mercari'"}
                try:
                    record["title"] = "'{}'".format(itm.find("span", class_="itemName__a6f874a2").get_text().replace("'", "_"))
                    if not judge_item(record["title"], set_number):
                        continue
                    record["price"] = "'{}'".format("".join(itm.find("span", class_="number__6b270ca7").get_text().split(",")))
                    record["url"] = "'{}'".format("https://jp.mercari.com" + itm.find("a", class_="sc-bcd1c877-1 lpjZwE")["href"])
                    record["date_modified"] = "'{}'".format(datetime.now())
                except:
                    continue
                records.append(record)

            next_page = False
            if next_page:
                pass
            else:
                page_unprocessed = False

    except AttributeError:
        return None
    return records


def crawl_yahoofurima(set_number):
    records = []
    page_unprocessed = True
    try:
        html = url2html("https://paypayfleamarket.yahoo.co.jp/search/LEGO%20{}?conditions=NEW&open=1".format(set_number))
        bs = BeautifulSoup(html, "html.parser")
        while page_unprocessed:
            for itm in bs.find(id="itm").find_all("a"):
                record = {"set_number":"'{}'".format(set_number), "site":"'yahoofurima'"}
                try:
                    record["title"] = "'{}'".format(itm.find("img")["alt"].replace("'", "_"))
                    if not judge_item(record["title"], set_number):
                        continue
                    record["price"] = "'{}'".format("".join(itm.find("p").get_text()[:-1].split(",")))
                    record["url"] = "'{}'".format("https://paypayfleamarket.yahoo.co.jp" + itm["href"])
                    record["date_modified"] = "'{}'".format(datetime.now())
                except:
                    continue
                records.append(record)
            
            next_page = False
            if next_page:
                pass
            else:
                page_unprocessed = False

    except AttributeError:
        return None
    return records
    

def crawl_rakuma(set_number):
    records = []
    page_unprocessed = True
    try:
        html = url2html("https://fril.jp/s?query=lego%20{}&status=new&transaction=selling".format(set_number))
        bs = BeautifulSoup(html, "html.parser")
        while page_unprocessed:
            for itm in bs.find_all("div", class_="item"):
                record = {"set_number":"'{}'".format(set_number), "site":"'rakuma'"}
                try:
                    record["title"] = "'{}'".format(itm.find("a", class_="link_search_title").find("span").get_text().replace("'", "_"))
                    if not judge_item(record["title"], set_number):
                        continue
                    record["price"] = "'{}'".format("".join(itm.find("p", class_="item-box__item-price").find_all("span")[1].get_text().split(",")))
                    record["url"] = "'{}'".format(itm.find("a", class_="link_search_title")["href"])
                    record["date_modified"] = "'{}'".format(datetime.now())
                except:
                    continue
                records.append(record)

            next_page = False
            if next_page:
                pass
            else:
                page_unprocessed = False

    except AttributeError:
        return None
    return records


def crawl_yahooauction(set_number):
    records = []
    page_unprocessed = True
    try:
        html = url2html("https://auctions.yahoo.co.jp/search/search?p=lego+{}&va=lego+{}&istatus=1&is_postage_mode=1&dest_pref_code=13&exflg=1&b=1&n=50".format(set_number, set_number))
        bs = BeautifulSoup(html, "html.parser")
        while page_unprocessed:
            for itm in bs.find_all("li", class_="Product"):
                record = {"set_number":"'{}'".format(set_number), "site": "'yahooauction'"}
                try:
                    record["title"] = "'{}'".format(itm.find("a", class_="Product__titleLink js-browseHistory-add js-rapid-override").get_text().replace("'", "_"))
                    if not judge_item(record["title"], set_number):
                        continue
                    record["price"] = "'{}'".format("".join(itm.find("span", class_="Product__priceValue u-textRed").get_text()[:-1].split(",")))
                    record["url"] = "'{}'".format(itm.find("a", class_="Product__titleLink js-browseHistory-add js-rapid-override")["href"])
                    record["date_modified"] = "'{}'".format(datetime.now())
                except:
                    continue
                records.append(record)

            next_page = False
            if next_page:
                pass
            else:
                page_unprocessed = False

    except AttributeError:
        return None
    return records

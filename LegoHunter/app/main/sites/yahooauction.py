from datetime import datetime
from bs4 import BeautifulSoup
from . import Site

class yahooauction(Site):

    def crawl(self, set_number):
        records = []
        page_unprocessed = True
        try:
            html = self.url2html("https://auctions.yahoo.co.jp/search/search?p=LEGO+{}&va=LEGO+{}&istatus=1&is_postage_mode=1&dest_pref_code=13&exflg=1&b=1&n=50".format(set_number, set_number))
            bs = BeautifulSoup(html, "html.parser")
            while page_unprocessed:
                for itm in bs.find_all("li", class_="Product"):
                    record = {"set_number": set_number, "site": "yahooauction"}
                    try:
                        record["title"] = itm.find("a", class_="Product__titleLink js-browseHistory-add js-rapid-override").get_text()
                        if not self.determine_item(record["title"], set_number):
                            continue
                        record["price"] = "".join(itm.find("span", class_="Product__priceValue u-textRed").get_text()[:-1].split(","))
                        record["url"] = itm.find("a", class_="Product__titleLink js-browseHistory-add js-rapid-override")["href"]
                        record["date_modified"] = datetime.now()
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
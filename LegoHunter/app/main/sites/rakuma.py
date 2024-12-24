from datetime import datetime
from bs4 import BeautifulSoup
from . import Site
class rakuma(Site):

    def crawl(self, set_number):
        records = []
        page_unprocessed = True
        try:
            html = self.url2html("https://fril.jp/s?query=LEGO%20{}&status=new&transaction=selling".format(set_number))
            bs = BeautifulSoup(html, "html.parser")
            while page_unprocessed:
                for itm in bs.find_all("div", class_="item"):
                    record = {"set_number": set_number, "site":"rakuma"}
                    try:
                        record["title"] = itm.find("a", class_="link_search_title").find("span").get_text()
                        if not self.determine_item(record["title"], set_number):
                            continue
                        record["price"] = "".join(itm.find("p", class_="item-box__item-price").find_all("span")[1].get_text().split(","))
                        record["url"] = itm.find("a", class_="link_search_title")["href"]
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

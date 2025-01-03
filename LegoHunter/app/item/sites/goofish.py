from datetime import datetime
from bs4 import BeautifulSoup
from . import Site


class goofish(Site):

    def crawl(self, set_number):
        records = []
        page_unprocessed = True
        try:
            html = self.url2html("https://www.goofish.com/search?q=LEGO%20{}".format(set_number))
            bs = BeautifulSoup(html, "html.parser")
            while page_unprocessed:
                for itm in bs.find_all("a", class_="feeds-item-wrap--rGdH_KoF"):
                    record = {"set_number": set_number, "site": "goofish"}
                    try:
                        record["title"] = "'{}'".format(itm.find("span", class_="main-title--sMrtWSJa").get_text().replace("'", "_"))
                        if not self.determine_item(record["title"], set_number):
                            continue
                        record["price"] = itm.find("span", class_="number--NKh1vXWM").get_text()
                        record["url"] = itm["href"]
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
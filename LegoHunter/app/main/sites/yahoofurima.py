from datetime import datetime
from bs4 import BeautifulSoup
from . import Site


class yahoofurima(Site):

    def crawl(self, set_number):
        records = []
        page_unprocessed = True
        try:
            html = self.url2html("https://paypayfleamarket.yahoo.co.jp/search/LEGO%20{}?conditions=NEW&open=1".format(set_number))
            bs = BeautifulSoup(html, "html.parser")
            while page_unprocessed:
                for itm in bs.find(id="itm").find_all("a"):
                    record = {"set_number": set_number, "site":"yahoofurima"}
                    try:
                        record["title"] = itm.find("img")["alt"]
                        if not self.determine_item(record["title"], set_number):
                            continue
                        record["price"] = "".join(itm.find("p").get_text()[:-1].split(","))
                        record["url"] = "https://paypayfleamarket.yahoo.co.jp" + itm["href"]
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
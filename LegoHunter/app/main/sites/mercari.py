from datetime import datetime
from bs4 import BeautifulSoup
from . import Site

class mercari(Site):

    def crawl(self, set_number):
        records = []
        page_unprocessed = True
        try:
            html = self.url2html("https://jp.mercari.com/search?keyword=LEGO%20{}&item_condition_id=1&status=on_sale".format(set_number), "selenium")
            bs = BeautifulSoup(html, "html.parser")
            while page_unprocessed:
                for itm in bs.find_all("li", class_="sc-bcd1c877-2 cvAXgx"):
                    record = {"set_number": set_number, "site":"mercari"}
                    try:
                        record["title"] = itm.find("span", class_="itemName__a6f874a2").get_text()
                        if not self.determine_item(record["title"], set_number):
                            continue
                        record["price"] = "".join(itm.find("span", class_="number__6b270ca7").get_text().split(","))
                        record["url"] = "https://jp.mercari.com" + itm.find("a", class_="sc-bcd1c877-1 lpjZwE")["href"]
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
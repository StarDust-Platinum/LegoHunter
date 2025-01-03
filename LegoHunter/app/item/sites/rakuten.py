from datetime import datetime
from bs4 import BeautifulSoup
from . import Site

class rakuten(Site):
    
    def crawl(self, set_number):
        records = []
        page_unprocessed = True
        try:
            html = self.url2html(r"https://search.rakuten.co.jp/search/mall/LEGO+{}/".format(set_number))
            bs = BeautifulSoup(html, "html.parser")
            while page_unprocessed:
                for itm in bs.find_all("div", class_="dui-card searchresultitem overlay-control-wrapper--2W6PV title-control-wrapper--1YBX9"):
                    record = {"set_number": set_number, "site":"rakuten"}
                    try:
                        record["title"] = itm.find("h2", class_="title-link-wrapper--2sUFJ title-link-wrapper-grid--db8v2").get_text()
                        if not self.judge_item(record["title"], set_number):
                            continue
                        record["price"] = "".join(itm.find("div", class_="price--OX_YW").get_text()[:-1].split(","))
                        record["url"] = itm.find("h2", class_="title-link-wrapper--2sUFJ title-link-wrapper-grid--db8v2").find("a")["href"]
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
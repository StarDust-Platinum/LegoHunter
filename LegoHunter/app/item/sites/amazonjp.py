from datetime import datetime
from bs4 import BeautifulSoup
from . import Site

class amazonjp(Site):
    
    def crawl(self, set_number):
        records = []
        page_unprocessed = True
        try:
            html = self.url2html(r"https://www.amazon.co.jp/s?k=LEGO+{}&__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&crid=2IGP4U26DZPY4&sprefix=LEGO+{}%2Caps%2C151&ref=nb_sb_noss_1".format(set_number, set_number))
            bs = BeautifulSoup(html, "html.parser")
            while page_unprocessed:
                for itm in bs.find_all("div", class_="sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20"):
                    record = {"set_number": set_number, "site":"amazonjp"}
                    try:
                        record["title"] = itm.find("span", class_="a-size-base-plus a-color-base a-text-normal").get_text()
                        if not self.determine_item(record["title"], set_number):
                            continue
                        record["price"] = "".join(itm.find("span", class_="a-offscreen").get_text()[1:].split(","))
                        record["url"] = "https://www.amazon.co.jp" + itm.find("a", class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal")["href"]
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

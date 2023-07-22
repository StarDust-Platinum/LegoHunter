from datetime import datetime
from crawler import crawl_set, crawl_item_from_mercari, crawl_item_from_paypay
import MySQLdb

if __name__=="__main__":
    lego_item_rows = []
    rows = crawl_item_from_mercari("42056")
    print(rows)
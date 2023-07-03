from datetime import datetime
import pymysql
from crawler import crawl_set, crawl_item_from_paypay

if __name__=="__main__":
    headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
    with open("db_settings.txt") as f:
        [db_user, db_pw, db_name,] = [line[:-1] for line in f.readlines() if line != '']
    with open("set_id_list.txt") as f:
        set_id_list = [set_id [:-1] for set_id in f.readlines() if set_id != '']
    for set_id in set_id_list:
        lego_set_row = crawl_set(set_id, headers)
        lego_item_rows = crawl_item_from_paypay(set_id, headers)
        connection = pymysql.connect(host="localhost",
                               user=db_user,
                               passwd=db_pw,
                               database=db_name,
                               charset="utf8",
                               cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:

                """
                UPDATE lego_set
                """
                cursor.execute("SELECT COUNT(*) FROM lego_set WHERE set_id={}".format(set_id))
                if cursor.fetchone()["COUNT(*)"] !=0 :
                    cursor.execute("UPDATE lego_set SET value='{}', last_updated='{}' WHERE set_id='{}'".format(lego_set_row["value"], datetime.now(), lego_set_row["set_id"]))
                else:
                    cursor.execute("INSERT INTO lego_set VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(lego_set_row["set_id"], lego_set_row["name"], lego_set_row["theme"], 
                                                                                                                               lego_set_row["year"], lego_set_row["pieces"], lego_set_row["availability"], 
                                                                                                                               lego_set_row["retail"], lego_set_row["value"], datetime.now()))
                """
                UPDATE lego_item
                """
                if lego_item_rows:
                    for lego_item_row in lego_item_rows:
                        cursor.execute("SELECT * FROM lego_item WHERE url='{}'".format(lego_item_row["url"]))
                        if cursor.fetchone():
                            cursor.execute("UPDATE lego_item SET title='{}', price='{}', last_updated='{}' WHERE url='{}'".format(lego_item_row["title"], lego_item_row["price"], datetime.now(), lego_item_row["url"]))
                        else:
                            cursor.execute("INSERT INTO lego_item (set_id, title, price, url, last_updated) VALUES ('{}', '{}', '{}', '{}', '{}')".format(lego_item_row['set_id'], lego_item_row['title'],
                                                                                                                                                            lego_item_row['price'], lego_item_row['url'],
                                                                                                                                                            datetime.now()))
            connection.commit()
        print(set_id+" completed")
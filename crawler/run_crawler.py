import os
from datetime import datetime
import MySQLdb
from crawler import crawl_set, crawl_amazonjp, crawl_rakuten, crawl_mercari, crawl_paypayfurima


if __name__=="__main__":
    with open(os.path.dirname(os.path.realpath(__file__))+"/db_settings.txt") as f:
        [db_user, db_pw, db_name,] = [line[:-1] for line in f.readlines() if line != '']
    with open(os.path.dirname(os.path.realpath(__file__))+"/set_id_list.txt") as f:
        set_id_list = [set_id [:-1] for set_id in f.readlines() if set_id != '']
    for set_id in set_id_list:
        lego_set_row = crawl_set(set_id)
        lego_item_rows = []
        lego_item_rows += crawl_amazonjp(set_id)
        lego_item_rows += crawl_rakuten(set_id)
        lego_item_rows += crawl_mercari(set_id)
        lego_item_rows += crawl_paypayfurima(set_id)

        connection = MySQLdb.connect(
            user=db_user,
            passwd=db_pw,
            host='localhost',
            db=db_name,
            charset="utf8")
        cursor = connection.cursor()

        #UPDATE lego set info
        keys = lego_set_row.keys()
        cursor.execute("SELECT COUNT(*) FROM lego_set WHERE set_id={}".format(set_id))
        if cursor.fetchone()[0] == 0:
            sql = "INSERT INTO lego_set (set_id, " + ",".join(keys) + ", last_updated) VALUES (" + ",".join(["'{}'"]*(len(keys)+2)) + ")"
            values = [ set_id ] + list(lego_set_row[key] for key in keys) + [ datetime.now() ]
            cursor.execute(sql.format(*values))
        else:
            if "value" in keys:
                sql = "UPDATE lego_set SET value='{}', last_updated='{}' WHERE set_id='{}'"
                values = [ lego_set_row["value"], datetime.now(), set_id ]
                cursor.execute(sql.format(*values))
                
        #UPDATE lego_item
        if lego_item_rows:
            for row in lego_item_rows:
                keys = row.keys()
                cursor.execute("SELECT * FROM lego_item WHERE url='{}'".format(row["url"]))
                if not cursor.fetchone():
                    sql = "INSERT INTO lego_item (set_id, " + ",".join(keys) + ", last_updated) VALUES (" + ",".join(["'{}'"]*(len(keys)+2)) + ")"
                    values = [ set_id ] + list(row[key] for key in keys) + [ datetime.now() ]
                    cursor.execute(sql.format(*values))
                else:
                    sql = "UPDATE lego_item SET title='{}', price='{}', last_updated='{}' WHERE url='{}'"
                    values = [ row["title"], row["price"], datetime.now(), row["url"] ]
                    cursor.execute(sql.format(*values))
        
        "DELETE PAST ITEMS"
        cursor.execute("DELETE FROM lego_item WHERE last_updated < NOW() - INTERVAL 1 DAY")
        
        connection.commit()
        cursor.close()
        connection.close()

        print(set_id+" completed")

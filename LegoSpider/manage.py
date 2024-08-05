from basictoolbox import load_config
from dbtoolbox import db_init, db_select, db_insert, db_update, db_delete
import crawler

config_loc = "/app/config.json"

if __name__=="__main__":

    config = load_config(config_loc)
    
    sites = config.pop("sites")
    set_numbers = config.pop("set_numbers")

    #db_init()

    for set_number in set_numbers:
        for site in sites.keys():
            if sites[site]:
                records = getattr(crawler, "crawl_" + site)(set_number)
                for record in records:
                    if db_select(config, "url", record["url"], "="):
                        db_update(config, record, "url", record["url"], "=")
                    else:
                        db_insert(config, record)
    #db_delete(config, "date_modified", "NOW() - INTERVAL 1 DAY", "<")

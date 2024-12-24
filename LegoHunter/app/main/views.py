import os
import json
import math
from flask import render_template, request, session, redirect, url_for, current_app
from .. import db
from ..models import Item
from . import main
from .sites import *


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route('/item')
def item():
    per_page = 50
    
    page = request.args.get('page', 1, type=int)
    
    page_max = math.ceil(Item.query.count()/50)

    if page > page_max:
        return redirect(url_for(".item", page=page_max))
    
    pagination = Item.query.order_by(Item.set_number.asc()).paginate(
        page=page, per_page=per_page, error_out=False)
    return render_template('item.html', pagination=pagination)


@main.route('/crawl')
def crawl():
    config_loc = os.getenv("CRAWLER_CONFIG_PATH")
    with open(config_loc, "r+") as f:
        config = json.load(f)
    site_list = config.pop("sites")
    set_numbers = config.pop("set_numbers")
    blacklist = config.pop("blacklist")

    for set_number in set_numbers.keys():

        if not set_numbers[set_number]:
            continue

        for site in site_list.keys():

            if not site_list[site]:
                continue
            
            crawler = getattr(globals()[site], site)(blacklist)
            records = crawler.crawl(set_number)
            if records:
                for record in records:
                    item = Item.query.filter_by(url=record["url"]).first()
                    if item:
                        item.set_number = record["set_number"]
                        item.site = record["site"]
                        item.title = record["title"]
                        item.price = record["price"]
                        item.url = record["url"]
                        item.date_modified = record["date_modified"]
                    else:
                        item = Item()
                        item.set_number = record["set_number"]
                        item.site = record["site"]
                        item.title = record["title"]
                        item.price = record["price"]
                        item.url = record["url"]
                        item.date_modified = record["date_modified"]
                    db.session.add(item)
                    db.session.commit()
    return render_template('crawl.html', text="Crawl is completed")
import math
from threading import Thread

from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user
from .. import db
from ..models import Set, Item, PriceExpectation
from ..decorators import admin_required
from . import item
from .forms import EditSetForm, CrawlConfigForm, SetPriceExpectationForm

from .sites import *


@item.route('/search')
def search():
    per_page = 50
    
    kw = request.args.get('kw')
    page = request.args.get('page', 1, type=int)
    
    page_max = math.ceil(Item.query.filter_by(id=search).count()/50)

    if page > page_max:
        return redirect(url_for(".search", kw=kw, page=page_max))
    
    pagination = Item.query.filter_by(set_number=kw).order_by(Item.set_number.asc()).paginate(
        page=page, per_page=per_page, error_out=False)
    return render_template('item/items.html', pagination=pagination)


@item.route('/items')
def items():
    per_page = 50
    
    page = request.args.get('page', 1, type=int)
    
    page_max = math.ceil(Item.query.count()/50)

    if page > page_max:
        return redirect(url_for(".items", page=page_max))
    
    pagination = Item.query.order_by(Item.set_number.asc()).paginate(
        page=page, per_page=per_page, error_out=False)
    return render_template('item/items.html', pagination=pagination)


@item.route('/set-price-expectation', methods=['GET', 'POST'])
def set_price_expectation():
    if current_user.is_anonymous:
        return redirect(url_for("auth.login"))
    
    form = SetPriceExpectationForm()
    if form.validate_on_submit():
        existing_expectation = PriceExpectation.query.filter_by(user_id=current_user.id, set_number=form.set_number.data).first()
        if existing_expectation:
            existing_expectation.price_expectation = form.price_expectation.data
            db.session.add(existing_expectation)
        else:
            new_expectation = PriceExpectation()
            new_expectation.user_id = current_user.id
            new_expectation.set_number = form.set_number.data
            new_expectation.price_expectation = form.price_expectation.data
            db.session.add(new_expectation)
        db.session.commit()
    expectations = PriceExpectation.query.filter_by(user_id=current_user.id)
    return render_template("item/set_price_expectation.html", form=form, expectations=expectations)


@item.route('/crawl', methods=['GET', 'POST'])
@admin_required
def crawl():
    edit_set_form = EditSetForm()
    if edit_set_form.edit_set_submit.data and edit_set_form.validate():
        existing_set = Set.query.filter_by(set_number=edit_set_form.set_number.data).first()
        
        if edit_set_form.set_number.data=='':
            flash('Plese Fill in the #')
        elif edit_set_form.operation.data == 'Add/Update':
            if existing_set:
                existing_set.name = edit_set_form.name.data
                db.session.add(existing_set)
            else:
                new_set = Set()
                new_set.set_number = edit_set_form.set_number.data
                new_set.name = edit_set_form.name.data
                db.session.add(new_set)
            db.session.commit()
        elif edit_set_form.operation.data == 'Delete':
            if existing_set:
                db.session.delete(existing_set)
                db.session.commit()
            else:
                flash('Set not registered!')
        else:
            flash('Error')
        return redirect(url_for(".crawl"))

    crawl_config_form = CrawlConfigForm()
    if crawl_config_form.crawl_config_submit.data and crawl_config_form.validate():
        if crawl_config_form.sites.data and crawl_config_form.sets.data:
            _crawl(crawl_config_form.sites.data, crawl_config_form.sets.data, crawl_config_form.filter_blacklist.data)
            #Thread(target=_crawl, args=(crawl_config_form.sites.data, crawl_config_form.sets.data, crawl_config_form.filter_blacklist.data)).start()
            flash("Crawl has started!")
        else:
            flash('Sites or sets not selected!')
        return redirect(url_for(".crawl"))

    return render_template('item/crawl.html', edit_set_form=edit_set_form, crawl_config_form=crawl_config_form)


def _crawl(sites, sets, filter_blacklist):
    for set_number in sets:
        for site in sites:
            crawler = getattr(globals()[site], site)(filter_blacklist)
            records = crawler.crawl(set_number)
            if records:
                for record in records:
                    item = Item.query.filter_by(url=record["url"]).first()
                    if item:
                        old_price = item.price

                        item.set_number = record["set_number"]
                        item.site = record["site"]
                        item.title = record["title"]
                        item.price = record["price"]
                        item.url = record["url"]
                        item.date_modified = record["date_modified"]
                        db.session.add(item)
                        db.session.commit()
                        if item.price<old_price:
                            _send_notification(record)
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
                        _send_notification(record)


def _send_notification(record):
    for price_expectation in PriceExpectation.query.all():
        if int(price_expectation.set_number)==int(record["set_number"]) and int(price_expectation.price_expectation)>=int(record["price"]):
            #sendemail()
            print(f"send email to user{price_expectation.user_id} content {price_expectation.set_number} price is {record['price']}")

import os, math
from threading import Thread
import http.client, urllib

from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .. import db
from ..models import User, Set, Item, PriceExpectation
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
@login_required
def set_price_expectation():
    if current_user.is_anonymous:
        return redirect(url_for("auth.login"))
    
    blank_form = SetPriceExpectationForm()
    forms = [ blank_form ]
    expectations = PriceExpectation.query.filter_by(user_id=current_user.id).all()
    for exp in expectations:
        form = SetPriceExpectationForm()
        form.set_number.data = exp.set_number
        form.price_expectation.data = exp.price_expectation
        forms.append(form)

    for form in forms:
        if form.add.data and form.validate_on_submit():
            if form.set_number.data=='':
                flash('Plese Fill in the #')
                return redirect(url_for('.set_price_expectation'))
            else:
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
        if form.delete.data and form.validate_on_submit():
            if form.set_number.data=='':
                flash('Plese Fill in the #')
                return redirect(url_for('.set_price_expectation'))
            else:
                existing_expectation = PriceExpectation.query.filter_by(user_id=current_user.id, set_number=form.set_number.data).first()
            if existing_expectation:
                db.session.delete(existing_expectation)
                db.session.commit()
            else:
                flash('Expectation not set!')
    return render_template("item/set_price_expectation.html", forms=forms)


@item.route('/manage-set', methods=['GET', 'POST'])
@admin_required
def manage_set():
    blank_form = EditSetForm()
    forms = [ blank_form ]
    sets = Set.query.all()
    for s in sets:
        form = EditSetForm()
        form.set_number.data = s.set_number
        form.name.data = s.name
        forms.append(form)

    for form in forms:
        if form.add.data and form.validate():
            if form.set_number.data=='':
                flash('Plese Fill in the #')
                return redirect(url_for(".manage_set"))
            else:
                existing_set = Set.query.filter_by(set_number=form.set_number.data).first()
            if existing_set:
                existing_set.name = form.name.data
                db.session.add(existing_set)
            else:
                new_set = Set()
                new_set.set_number = form.set_number.data
                new_set.name = form.name.data
                db.session.add(new_set)
            db.session.commit()
            return redirect(url_for(".manage_set"))
        if form.delete.data and form.validate():
            if form.set_number.data=='':
                flash('Plese Fill in the #')
                return redirect(url_for(".manage_set"))
            else:
                existing_set = Set.query.filter_by(set_number=form.set_number.data).first()
            if existing_set:
                db.session.delete(existing_set)
                db.session.commit()
            else:
                flash('Set not registered!')
            return redirect(url_for(".manage_set"))
    return render_template('item/manage_set.html', forms=forms)


@item.route('/manage-crawl', methods=['GET', 'POST'])
@admin_required
def manage_crawl():
    crawl_config_form = CrawlConfigForm()
    if crawl_config_form.submit.data and crawl_config_form.validate():
        if crawl_config_form.sites.data and crawl_config_form.sets.data:
            _crawl(crawl_config_form.sites.data, crawl_config_form.sets.data, crawl_config_form.filter_blacklist.data.split(','))
            #Thread(target=_crawl, args=(crawl_config_form.sites.data, crawl_config_form.sets.data, crawl_config_form.filter_blacklist.data)).start()
            flash("Crawl has started!")
        else:
            flash('Sites or sets not selected!')
        return redirect(url_for(".manage_crawl"))
    return render_template('item/manage_crawl.html', crawl_config_form=crawl_config_form)


@item.route('/crawl-cron', methods=['POST'])
def crawl_cron():
    site_list = request.json["site_list"]
    set_list = [ str(_.set_number) for _ in Set.query.all() ]
    filter_blacklist = os.environ.get('FILTER_BLACKLIST').split(',')
    _crawl(site_list, set_list, filter_blacklist)
    return "cron job complete!"


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
            APP_TOKEN = os.environ.get('APP_TOKEN')
            USER_KEY = User.query.filter_by(id = price_expectation.user_id).first().userkey
            MESSAGE = f"{record['set_number']}: {record['price']}"
            URL = record["url"]
            if USER_KEY:
                _pushover(APP_TOKEN, USER_KEY, MESSAGE, URL)


def _pushover(APP_TOKEN, USER_KEY, MESSAGE, URL):
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
    urllib.parse.urlencode({
        "token": APP_TOKEN,
        "user": USER_KEY,
        "message": MESSAGE,
        "url": URL,
    }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()

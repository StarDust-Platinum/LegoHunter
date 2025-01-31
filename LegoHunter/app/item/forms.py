import os

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField, widgets
from ..models import Set
from .sites import __all__ as site_list


class SetPriceExpectationForm(FlaskForm):
    set_number = StringField('')
    price_expectation = StringField('')
    add = SubmitField('Add')
    delete = SubmitField('Delete')


class EditSetForm(FlaskForm):
    set_number = StringField('')
    name = StringField('')
    add = SubmitField('Add')
    delete = SubmitField('Delete')


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

    
class CrawlConfigForm(FlaskForm):
    filter_blacklist_default = os.environ.get('FILTER_BLACKLIST')

    sites = MultiCheckboxField('Sites')
    sets = MultiCheckboxField('Sets')
    filter_blacklist = StringField('Filter out', default=filter_blacklist_default)
    submit = SubmitField('Submit')

    def __init__(self):
        super(CrawlConfigForm, self).__init__()
        self.sites.choices = [ (site, site) for site in site_list ]
        self.sets.choices = [((lego_set.set_number), str(lego_set.set_number)) for lego_set in Set.query.all()]

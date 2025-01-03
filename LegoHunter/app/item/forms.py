from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField, SelectMultipleField, widgets
from ..models import Set
from .sites import __all__ as site_list


class SetPriceExpectationForm(FlaskForm):
    set_number = StringField('#')
    price_expectation = StringField('JPY')
    submit = SubmitField('Submit')


class EditSetForm(FlaskForm):
    set_number = StringField('#')
    name = StringField('name')
    operation = RadioField('operation', choices=[('Add/Update', 'Add/Update'), ('Delete', 'Delete')], default='Add/Update')
    edit_set_submit = SubmitField('Submit')


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

    
class CrawlConfigForm(FlaskForm):
    filter_blacklist_default = "说明书,图纸,兼容,互換,LED,展示盒,ケース"

    sites = MultiCheckboxField('Sites')
    sets = MultiCheckboxField('Sets')
    filter_blacklist = StringField('Filter out', default=filter_blacklist_default)
    crawl_config_submit = SubmitField('Submit')

    def __init__(self):
        super(CrawlConfigForm, self).__init__()
        self.sites.choices = [ (site, site) for site in site_list ]
        self.sets.choices = [((lego_set.set_number), str(lego_set.set_number)) for lego_set in Set.query.all()]

#from django.shortcuts import render
from django.views.generic.list import ListView
from items.models import LegoItem

class LegoItemListView(ListView):
    model = LegoItem
    paginate_by = 20  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

from django.shortcuts import render
from django.core.paginator import Paginator
from items.models import LegoItem

from django.views.generic.list import ListView

def index(request):
    context = {}
    context["items"] = LegoItem.objects.all()
    return render(
        request, "index.html", context
    )

class LegoItemListView(ListView):
    model = LegoItem
    paginate_by = 20  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

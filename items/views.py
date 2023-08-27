from django.core.paginator import Paginator
from django.shortcuts import render
from items.models import LegoItem

def items(request):
    context = {}
    item_list = LegoItem.objects.all()
    sort = request.GET.get('sort')
    order = request.GET.get('order')
    try:
        if order == "asc":
            item_list = item_list.order_by(sort)
        elif order == "desc":
            item_list = item_list.order_by("-" + sort)
        else:
            item_list = item_list.order_by(sort)
    except:
        pass
    paginator = Paginator(item_list, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context["page_obj"] = page_obj
    return render(request, "items/items.html", context)

def search(request):
    context = {}
    search_word = request.GET.get('kw', '')
    sort = request.GET.get('sort')
    order = request.GET.get('order')
    item_list = LegoItem.objects.filter(title__icontains=search_word)
    try:
        if order == "asc":
            item_list = item_list.order_by(sort)
        elif order == "desc":
            item_list = item_list.order_by("-" + sort)
        else:
            item_list = item_list.order_by(sort)
    except:
        pass
    paginator = Paginator(item_list, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context["page_obj"] = page_obj
    context["kw"] = search_word
    return render(request, 'items/search.html', context)
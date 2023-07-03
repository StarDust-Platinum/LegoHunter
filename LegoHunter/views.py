from django.shortcuts import render
import pymysql
import LegoHunter.settings as settings

def index(request):
    context = {}
    connection = pymysql.connect(host="localhost",
                                user=settings.DB_USER,
                                passwd=settings.DB_PW,
                                database=settings.DB_NAME,
                                charset="utf8",
                                cursorclass=pymysql.cursors.DictCursor)
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT lego_item.set_id, lego_item.price, lego_item.title, lego_item.url, lego_set.name FROM lego_item, lego_set WHERE lego_item.set_id=lego_set.set_id ORDER BY set_id")
            item_list = cursor.fetchall()
    context["item_list"] = item_list
    return render(
        request, "index.html", context
    )
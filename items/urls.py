from django.urls import path
from . import views

urlpatterns = [
    path('', views.LegoItemListView.as_view()),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.items),
    path('search/', views.search, name="search")
]
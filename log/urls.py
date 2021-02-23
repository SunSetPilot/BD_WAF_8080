from django.urls import path
from . import views

urlpatterns = [
    path('getalllog', views.get_all_log),
    path('getselectedlog', views.get_selected_log),
    path('getdetailedlog', views.get_detailed_log),
]
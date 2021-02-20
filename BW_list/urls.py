from django.urls import path
from . import views

urlpatterns = [
    path('getwhiteip',views.get_white_ip),
    path('getblackip',views.get_black_ip),
    path('getwhiteurl',views.get_white_url),
    path('getblackurl',views.get_black_url),
    path('addbw',views.add_bw),
    path('dellist',views.del_list),
    path('changebwip',views.change_bw_ip),
    path('changebwurl',views.change_bw_url),
]

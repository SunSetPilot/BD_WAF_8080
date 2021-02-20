from django.urls import path
from . import views

urlpatterns = [
    path('getallrules',views.get_all_rules),
    path('getselectedrules',views.get_selected_rules),
    path('addrule',views.add_rules),
    path('delrule',views.del_rules),

]
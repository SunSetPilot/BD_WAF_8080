from django.urls import path
from . import views

urlpatterns = [
    path('getrulefiles',views.get_rule_files),
    path('delrulefile',views.del_rule_file),
    path('addfile',views.add_file),
    path('editfile',views.edit_file),
]
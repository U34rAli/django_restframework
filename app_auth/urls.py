from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('exampleview', views.example_view, name='exampleview'),
    path('registeruser', views.register_user, name='registeruser'),
    path('registeruser', views.register_user, name='gauth'),
    path('validatetoken', views.validate_token, name='validatetoken'),
    path('getdata', views.knox_validation, name='knoxgetdata'),
]

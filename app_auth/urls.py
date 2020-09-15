from django.urls import path
from knox import views as knox_views

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('exampleview', views.example_view, name='exampleview'),
    path('registeruser', views.register_user, name='registeruser'),
    path('registeruser', views.register_user, name='gauth'),
    path('validatetoken', views.validate_token, name='validatetoken'),
    path('getdata', views.knox_validation, name='knoxgetdata'),
    path('logoutall', knox_views.LogoutAllView.as_view(), name='knox_logoutall')
]

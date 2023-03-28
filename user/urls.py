from django.urls import path

from . import views

urlpatterns = [
    path('login', views.login),
    path('verify_token', views.verify_token),
    path('fetch_data', views.fetch_data),
    path('ask', views.ask),
    path('clear', views.clear),
]

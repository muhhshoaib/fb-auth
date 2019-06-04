"""fbapp URL Configuration"""

from django.urls import path
from src.apps.fbapp import views


urlpatterns = [
    path('deauthorize', views.DeauthorizeView.as_view(), name='deactivate'),
]


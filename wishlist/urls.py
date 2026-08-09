from django.urls import path
from . import views

app_name = 'wishlist'

urlpatterns = [
    path('', views.view_wishlist, name='view'),
    path('api/toggle/', views.toggle_wishlist_api, name='toggle_api'),
]

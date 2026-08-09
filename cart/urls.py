from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.view_cart, name='view'),
    path('api/add/', views.add_to_cart_api, name='add_api'),
    path('api/update/', views.update_cart_api, name='update_api'),
    path('apply-coupon/', views.apply_coupon, name='apply_coupon'),
]

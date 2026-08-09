from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('order/<int:order_id>/update-status/', views.update_order_status, name='update_order_status'),
    path('api/order-status/', views.update_order_status_api, name='update_order_status_api'),
]

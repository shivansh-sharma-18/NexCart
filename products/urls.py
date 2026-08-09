from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.catalog, name='catalog'),
    path('api/search-suggest/', views.search_suggest_api, name='search_suggest_api'),
    path('api/quick-view/<int:product_id>/', views.quick_view_api, name='quick_view_api'),
    path('<slug:slug>/', views.detail, name='detail'),
]

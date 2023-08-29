from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    # Categories API's
    path('api/category/list', views.CategoryAPIView().as_view(), name='category_list'),
    path('api/category/create', views.CategoryCreateView().as_view(), name='category_create'),
    path('api/<uuid:pk>/category', views.CategoryAPIView().as_view(), name='category'),
    
    # Food items API's
    path('api/food/item/list', views.FoodItemAPIView().as_view(), name='category_list'),
    path('api/food/item/create', views.FoodItemCreateView().as_view(), name='category_create'),
    path('api/<uuid:pk>/food/item/', views.FoodItemAPIView().as_view(), name='category'),
]
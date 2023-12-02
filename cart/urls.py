from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    # Cart API's
    path('api/items', views.CartCreateView().as_view(), name='cart'),
    
    # path('api/category/create', views.CategoryCreateView().as_view(), name='category_create'),
    # path('api/<uuid:pk>/category', views.CategoryAPIView().as_view(), name='category'),
    
    # Cart Item API's
    # path('api/food/item/list', views.FoodItemAPIView().as_view(), name='category_list'),
    # path('api/food/item/create', views.FoodItemCreateView().as_view(), name='category_create'),
    # path('api/<uuid:pk>/food/item/', views.FoodItemAPIView().as_view(), name='category'),
]
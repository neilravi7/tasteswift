from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    # Categories API's
    path('api/category/list', views.CategoryAPIView().as_view(), name='category_list'),
    path('api/category/create', views.CategoryCreateView().as_view(), name='category_create'),
    path('api/<uuid:pk>/category', views.CategoryAPIView().as_view(), name='category'),
    
    # Food items API's
    path('api/food/item/list', views.FoodItemListView().as_view(), name='food_item_list'),
    path('api/food/<uuid:pk>/items', views.FoodItemCustomerAPIView().as_view(), name='food_item_list_customer'),    
    path('api/food/item/create', views.FoodItemCreateView().as_view(), name='food_item_create'),
    path('api/food/item/<uuid:pk>/', views.FoodItemAPIView().as_view(), name='food_item'),
]
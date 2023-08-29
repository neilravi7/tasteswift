from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView
from . import views

app_name = 'accounts'

urlpatterns = [
    # AUTH URLS:
    path('accounts/api/user/signup', views.SignUpView.as_view(), name='signup'),
    path('accounts/api/user/signin', views.LoginView.as_view(), name='signin'),
    path('accounts/api/user/signout', views.LogoutView.as_view(), name='signout'),
    path('accounts/api/user/signin/refresh', TokenRefreshView.as_view(), name='token_refresh'),

    # # USER URLS:
    # # User List
    # path('api/users/list', views.UserList.as_view(), name='user_list'),
    #  # User Details
    # path('api/users/<uuid:pk>/info', views.UserDetail.as_view(), name='user_details'),
    
    # # User Deletion
    # path('api/users/<uuid:pk>/delete', views.UserDelete.as_view(), name='user_delete'),
    
    # # User Partial Update
    # path('api/users/<uuid:pk>/update-partial', views.UserPartialUpdate.as_view(), name='user_partial-update'),

    # # Change password view
    # path('api/users/<uuid:pk>/update-password', views.ChangePasswordView.as_view(), name='change_password'),
]
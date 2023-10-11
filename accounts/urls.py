from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views import (
    UserRegistrationView,
    RiderRegistrationView,
    RestaurantRegistrationView,
    UserLoginView,
    UserListView
)

urlpatterns = [
    path('token/obtain', jwt_views.TokenObtainPairView.as_view(), name='token_create'),
    path('token/refresh', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('account/register/user', UserRegistrationView.as_view(), name='register_user'),
    path('account/register/rider', RiderRegistrationView.as_view(), name='register_rider'),
    path('account/register/restaurant', RestaurantRegistrationView.as_view(), name='register_restaurant'),
    path('account/login', UserLoginView.as_view(), name='login'),
    path('account/registered-users/list', UserListView.as_view(), name='users')
]
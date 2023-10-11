from django.urls import path

from .views import CreateRestaurantView, UpdateRestaurantView, AddCuisineToRestaurantView, AddMenuItemToRestaurantView, RestaurantSuggestionView, RestaurantMenuAPIView, NearestRiderView

urlpatterns = [
    path('restaurant/create', CreateRestaurantView.as_view(), name='create-restaurant'),
    path('restaurant/update/<int:pk>', UpdateRestaurantView.as_view(), name='update-restaurant'),
    path('restaurant/<int:restaurant_id>/add-cuisine', AddCuisineToRestaurantView.as_view(), name='add-cuisine'),
    path('restaurant/<int:restaurant_id>/add-menu-item', AddMenuItemToRestaurantView.as_view(), name='add-menu-item'),
    path('restaurant/suggest_restaurants', RestaurantSuggestionView.as_view(), name='suggest_restaurants'),
    path('restaurant/<int:restaurant_id>/menu', RestaurantMenuAPIView.as_view(), name='restaurant-menu'),
    path('restaurant/nearest-rider/<int:restaurant_id>/<int:order_id>', NearestRiderView.as_view(), name='nearest-rider'),
]


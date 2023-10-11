from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from permissions import IsRestaurantRole
from rider.models import Rider
from orders.models import Order

from .serializers import (
   RestaurantSerializer,
   CuisineSerializer,
   MenuSerializer,
   RestaurantSuggestionSerializer,
   NearestRiderSerializer
)

from .models import Restaurant, Menu


class CreateRestaurantView(APIView):
   
    """
    API view for creating a restaurant.

    Attributes:
        permission_classes (tuple): Tuple of permission classes.
    """

    permission_classes = (IsAuthenticated, IsRestaurantRole)

    def post(self, request):
        """
        Handles creating a new restaurant.

        Args:
            request (Request): HTTP request.

        Returns:
            Response: HTTP response with restaurant creation information.
        """

        data=request.data.copy()

        data["restaurant_manager"] = request.user.pk

        serializer = RestaurantSerializer(data=data)

        valid = serializer.is_valid(raise_exception=True)
        if valid:
            serializer.save()  # Assign the authenticated user as the owner of the restaurant
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateRestaurantView(APIView):
    
    """
    API view for updating a restaurant.

    Attributes:
        permission_classes (tuple): Tuple of permission classes.
    """

    permission_classes = (IsAuthenticated, IsRestaurantRole)
    
    def put(self, request, pk):
        """
        Handles updating an existing restaurant.

        Args:
            request (Request): HTTP request.
            pk (int): The primary key of the restaurant.

        Returns:
            Response: HTTP response with updated restaurant information.
        """

        restaurant = get_object_or_404(Restaurant, id=pk)

        if request.user != restaurant.restaurant_manager:
            return Response({'error': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)
        
        restaurant = get_object_or_404(Restaurant, pk=pk)
        serializer = RestaurantSerializer(restaurant, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddCuisineToRestaurantView(APIView):
    """
    API view for adding a cuisine to a restaurant.
    """

    permission_classes = (IsAuthenticated, IsRestaurantRole)

    def post(self, request, restaurant_id):
        """
        Handles adding a cuisine to a restaurant.

        Args:
            request (Request): HTTP request.
            restaurant_id (int): The ID of the restaurant.

        Returns:
            Response: HTTP response with information about the added cuisine.
        """

        restaurant = get_object_or_404(Restaurant, id=restaurant_id)

        # Check if the authenticated user is the manager of the restaurant
        if request.user != restaurant.restaurant_manager:
            return Response({'error': 'You are not authorized to add cuisines to this restaurant.'}, 
                            status=status.HTTP_403_FORBIDDEN)

        serializer = CuisineSerializer(data=request.data)
        if serializer.is_valid():
            
            cuisine = serializer.validated_data.get('name')
            existing_cuisine = restaurant.cuisines.filter(name=cuisine).first() 
            if existing_cuisine:
                return Response({'error': 'This cuisine already exists for the restaurant.'}, 
                                status=status.HTTP_400_BAD_REQUEST)

            # Create the cuisine and add it to the restaurant
            cuisine = serializer.save()
            restaurant.cuisines.add(cuisine)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class AddMenuItemToRestaurantView(APIView):
    """
    API view for adding a menu item to a restaurant.
    """

    permission_classes = (IsAuthenticated, IsRestaurantRole)

    def post(self, request, restaurant_id):
        """
        Handles adding a menu item to a restaurant.

        Args:
            request (Request): HTTP request.
            restaurant_id (int): The ID of the restaurant.

        Returns:
            Response: HTTP response with information about the added menu item.
        """
         
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)

        if request.user != restaurant.restaurant_manager:
            return Response({'error': 'You are not authorized to add menu items to this restaurant.'}, 
                            status=status.HTTP_403_FORBIDDEN)
        
        data = request.data.copy()
        data["restaurant"] = restaurant.pk

        serializer = MenuSerializer(data=data)
        if serializer.is_valid():
            item = serializer.validated_data.get('item')

            existing_menu = restaurant.menu_set.filter(item=item).first() 
            
            if existing_menu:
                serializer.update(existing_menu, serializer.validated_data)
            else:
                # Save the new menu item
                serializer.save(restaurant=restaurant)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class RestaurantSuggestionView(APIView):
    """
    API view for suggesting restaurants.

    Attributes:
        permission_classes (tuple): Tuple of permission classes.
    """

    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        """
        Handles suggesting restaurants based on kind_of_food and desired_time.

        Args:
            request (Request): HTTP request.

        Returns:
            Response: HTTP response with suggested restaurants.
        """

        serializer = RestaurantSuggestionSerializer(data=request.data)
        if serializer.is_valid():
            kind_of_food = serializer.validated_data.get('kind_of_food')
            desired_time = serializer.validated_data.get('desired_time')

            # Get restaurants based on kind_of_food and desired_time
            suggested_restaurants = Restaurant.objects.filter(
                cuisines__name__iexact=kind_of_food,
                opening_time__lte=desired_time,
                closing_time__gte=desired_time,
            )

            return Response({'suggested_restaurants': suggested_restaurants.values()}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class RestaurantMenuAPIView(APIView):
    """
    API view for getting a restaurant's menu.

    Attributes:
        permission_classes (tuple): Tuple of permission classes.
    """

    permission_classes = (IsAuthenticated,)
    
    def get(self, request, restaurant_id):
        
        """
        Handles retrieving the menu of a restaurant.

        Args:
            request (Request): HTTP request.
            restaurant_id (int): The ID of the restaurant.

        Returns:
            Response: HTTP response with the restaurant's menu.
        """

        try:
            menu = Menu.objects.filter(restaurant_id=restaurant_id)
            serializer = MenuSerializer(menu, many=True, included_fields=['item', 'price'])
            data = serializer.data
            return Response(data, status=status.HTTP_200_OK)
        except Menu.DoesNotExist:
            return Response({"message": "Menu not found for this restaurant."},
                            status=status.HTTP_404_NOT_FOUND)
        

class NearestRiderView(APIView):
    """
    API view for finding the nearest rider for an order.

    Attributes:
        permission_classes (tuple): Tuple of permission classes.
    """
    permission_classes = (IsAuthenticated, IsRestaurantRole)

    def get_riders_within_range(self, restaurant_latitude, restaurant_longitude, distance_range):
        """
        Finds riders within a specified distance range from a restaurant.

        Args:
            restaurant_latitude (float): Latitude of the restaurant.
            restaurant_longitude (float): Longitude of the restaurant.
            distance_range (float): Distance range in kilometers.

        Returns:
            QuerySet: Queryset of riders within the specified distance range.
        """

        return Rider.get_riders_within_range(restaurant_latitude, restaurant_longitude, distance_range)

    def assign_order_to_rider(self, order_id, nearest_rider):
        """
        Assigns an order to the nearest rider.

        Args:
            order_id (int): The ID of the order.
            nearest_rider (Rider): The nearest rider.

        Returns:
            bool: True if the order is successfully assigned, False otherwise.
        """

        order = get_object_or_404(Order, pk=order_id)
        if order.is_delivered:
            return False
        nearest_rider.order = order
        nearest_rider.is_picked_up = True
        nearest_rider.save()
        return True

    def get(self, request, restaurant_id, order_id):
        """
        Handles finding the nearest rider for an order.

        Args:
            request (Request): HTTP request.
            restaurant_id (int): The ID of the restaurant.
            order_id (int): The ID of the order.

        Returns:
            Response: HTTP response with the nearest rider information.
        """
        restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
        restaurant_latitude = float(restaurant.latitude)
        restaurant_longitude = float(restaurant.longitude)

        initial_range = 1  # Initial range in kilometers
        max_range = 2  # Maximum range in kilometers

        while initial_range <= max_range:
            riders = self.get_riders_within_range(restaurant_latitude, restaurant_longitude, initial_range)
            if riders.exists():
                nearest_rider = riders.first()  # Assuming the first rider is the nearest
                order_status = self.assign_order_to_rider(order_id, nearest_rider)  # Assign the order to the nearest rider
                if not order_status:
                    return Response({"error": "Order has already been delivered."}, status=status.HTTP_400_BAD_REQUEST)
                serializer = NearestRiderSerializer(nearest_rider)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                initial_range += 0.2  # Increase the range by 0.2km

        return Response({"message": "No riders available within the specified range."}, status=status.HTTP_404_NOT_FOUND)
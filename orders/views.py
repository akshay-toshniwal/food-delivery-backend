from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from restaurant.models import Restaurant, Menu

class CreateOrderAPIView(APIView):
    """
    API view to create an order.

    Attributes:
        permission_classes (tuple): Tuple of permission classes.
    """

    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        """
        Handles the creation of a new order.

        Args:
            request (Request): HTTP request.

        Returns:
            Response: HTTP response with order creation information.
        """
        # Extract data from the request
        restaurant_pk = request.data.get('restaurant_id')
        menu_items = request.data.get('menu_items', [])  # List of menu item names and quantities

        # Get the user creating the order
        user = request.user
        # Get the restaurant
        try:
            restaurant = Restaurant.objects.get(pk=restaurant_pk)
        except Restaurant.DoesNotExist:
            return Response({"error": f"Restaurant does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        # Create the order
        order = Order.objects.create(user=user, restaurant=restaurant)

        # Create order items
        for item in menu_items:
            menu_item_name = item.get('menu_item')
            quantity = item.get('quantity', 1)  # Default to 1 if quantity is not provided

            try:
                # Use filter to handle MultipleObjectsReturned
                menu_items_queryset = Menu.objects.filter(restaurant=restaurant, item=menu_item_name)
                if menu_items_queryset.exists():
                    for menu_item in menu_items_queryset:
                        OrderItem.objects.create(order=order, menu_item=menu_item, quantity=quantity)
                else:
                    return Response({"error": f"No menu item found for '{menu_item_name}' in the specified restaurant."}, status=status.HTTP_400_BAD_REQUEST)
            except Menu.MultipleObjectsReturned:
                return Response({"error": f"Multiple menu items found for '{menu_item_name}' in the specified restaurant."}, status=status.HTTP_400_BAD_REQUEST)

        # Serialize the order for response
        order.is_placed = True
        order.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UserOrderListView(APIView):
    """
    API view to retrieve orders associated with a user.

    Attributes:
        permission_classes (list): List of permission classes.
    """

    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        """
        Retrieves orders associated with the authenticated user.

        Args:
            request (Request): HTTP request.

        Returns:
            Response: HTTP response with order information.
        """
        # Retrieve orders associated with the authenticated user
        orders = Order.objects.filter(user=self.request.user)
        
        order_details_list = []
        for order in orders:
            order_serializer = OrderSerializer(order)
            order_item_serializer = OrderItemSerializer(order.items.all(), many=True)
            
            order_details = {
                "order": order_serializer.data,
                "order_items": order_item_serializer.data,
                "total_value": order.total_value
            }
            order_details_list.append(order_details)

        return Response(order_details_list, status=status.HTTP_200_OK)

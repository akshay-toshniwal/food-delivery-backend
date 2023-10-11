from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from permissions import IsRiderRole
from .models import Rider
from .serializers import RiderSerializer, OrderSerializer
from orders.models import Order

class RiderProfileUpdateView(APIView):
    """
    API view for updating rider profile.

    Attributes:
        permission_classes (tuple): The permission classes for the view.
    """

    permission_classes = (IsAuthenticated, IsRiderRole)

    def post(self, request):
        """
        Handle POST request to update rider profile.

        Args:
            request (Request): The request object.

        Returns:
            Response: The response containing updated rider profile data.
        """

        data=request.data.copy()

        data["rider"] = request.user.pk

        serializer = RiderSerializer(data=data)

        valid = serializer.is_valid(raise_exception=True)
        if valid:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

class RiderUpdateLocationView(APIView):
    """
    API view for updating rider location.

    Attributes:
        permission_classes (tuple): The permission classes for the view.
    """

    permission_classes = (IsAuthenticated, IsRiderRole)

    def post(self, request):
        """
        Handle POST request to update rider location.

        Args:
            request (Request): The request object.

        Returns:
            Response: The response indicating successful location update.
        """

        rider = get_object_or_404(Rider, rider=request.user)

        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')

        # Update rider's location
        rider.latitude = latitude
        rider.longitude = longitude
        rider.save()

        return Response({"message": "Rider location updated successfully."}, status=status.HTTP_200_OK)

class RiderUpdateOrderView(APIView):
    """
    API view for updating rider's order status.

    Attributes:
        permission_classes (tuple): The permission classes for the view.
    """

    permission_classes = (IsAuthenticated, IsRiderRole)

    def post(self, request):
        """
        Handle POST request to update rider's order status.

        Args:
            request (Request): The request object.

        Returns:
            Response: The response indicating successful order update.
        """
        
        rider = get_object_or_404(Rider, rider=request.user)

        if rider.order and not rider.order.is_delivered:
            rider.is_delivered = True
            rider.is_picked_up = False
            rider.order.is_delivered = True
            rider.order.save()  # Save changes to the Order model
            rider.save()  # Save changes to the Rider model

            return Response({'message': 'Order marked as delivered successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No order found or order is already delivered.'}, status=status.HTTP_400_BAD_REQUEST)
        
class RiderDeliveredOrdersView(APIView):
    """
    API view for retrieving delivered orders for a rider.

    Attributes:
        permission_classes (tuple): The permission classes for the view.
    """

    permission_classes = (IsAuthenticated, IsRiderRole)

    def get(self, request):
        """
        Handle GET request to retrieve delivered orders for a rider.

        Args:
            request (Request): The request object.

        Returns:
            Response: The response containing delivered order data.
        """

        rider = get_object_or_404(Rider, rider=request.user)

        # Retrieve delivered orders for this rider
        delivered_orders = Order.objects.filter(rider=rider, is_delivered=True)
        serializer = OrderSerializer(delivered_orders, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

from rest_framework import serializers
from .models import Rider
from orders.serializers import OrderSerializer

class RiderSerializer(serializers.ModelSerializer):
    """
    Serializer for the Rider model.

    Attributes:
        Meta (class): Metadata options for the serializer.
    """

    class Meta:
        model = Rider
        fields = '__all__'


class NearestRiderSerializer(serializers.Serializer):
    """
    Serializer for the nearest rider.

    Attributes:
        name (str): The name of the rider.
        phone_number (str): The phone number of the rider.
        latitude (Decimal): The latitude of the rider's location.
        longitude (Decimal): The longitude of the rider's location.
        order_id (int): The ID of the associated order.
        restaurant_name (str): The name of the associated restaurant.
    """

    name = serializers.SerializerMethodField()
    phone_number = serializers.SerializerMethodField()
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    order_id = serializers.SerializerMethodField()
    restaurant_name = serializers.SerializerMethodField()

    def get_name(self, obj):
        """
        Returns the full name of the rider.

        Args:
            obj (Rider): The Rider object.

        Returns:
            str: The full name of the rider.
        """
        return f"{obj.rider.first_name} {obj.rider.last_name}"

    def get_phone_number(self, obj):
        """
        Returns the phone number of the rider.

        Args:
            obj (Rider): The Rider object.

        Returns:
            str: The phone number of the rider.
        """
        return obj.rider.phone  # Assuming you have a phone field in your User model

    def get_order_id(self, obj):
        """
        Returns the ID of the associated order.

        Args:
            obj (Rider): The Rider object.

        Returns:
            int: The ID of the associated order.
        """
        if obj.order:
            return obj.order.id
        return None

    def get_restaurant_name(self, obj):
        """
        Returns the name of the associated restaurant.

        Args:
            obj (Rider): The Rider object.

        Returns:
            str: The name of the associated restaurant.
        """
        if obj.order and obj.order.restaurant:
            return obj.order.restaurant.restaurant_name
        return None

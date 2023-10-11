from rest_framework import serializers
from .models import Order, OrderItem

class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for the Order model.

    Attributes:
        user (int): The user placing the order.
        restaurant (int): The restaurant for the order.
        order_date (datetime): The date and time of the order.
        is_placed (bool): Indicates if the order is placed.
        is_delivered (bool): Indicates if the order is delivered.
    """

    class Meta:
        model = Order
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer for the OrderItem model.

    Attributes:
        menu_item_name (str): The name of the menu item in the order.
        menu_item_price (float): The price of the menu item in the order.
        quantity (int): The quantity of the menu item in the order.
    """

    menu_item_name = serializers.ReadOnlyField(source='menu_item.item')
    menu_item_price = serializers.ReadOnlyField(source='menu_item.price')

    class Meta:
        model = OrderItem
        fields = ['menu_item_name', 'menu_item_price', 'quantity']

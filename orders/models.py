from django.db import models
from django.utils import timezone
from restaurant.models import Restaurant, Menu
from accounts.models import User

class Order(models.Model):
    """
    Model for orders.

    Attributes:
        user (User): The user placing the order.
        restaurant (Restaurant): The restaurant for the order.
        order_date (datetime): The date and time of the order.
        is_placed (bool): Indicates if the order is placed.
        is_delivered (bool): Indicates if the order is delivered.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    order_date = models.DateTimeField(default=timezone.now)
    is_placed = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)

    @property
    def total_value(self):
        """
        Calculates the total value of the order.

        Returns:
            float: The total value of the order.
        """
        total_value = 0
        for item in self.items.all():
            total_value += item.menu_item.price * item.quantity
        return total_value

    def __str__(self):
        """
        Returns a string representation of the order.

        Returns:
            str: String representation of the order.
        """
        return f"Order {self.id} by {self.user.email} at {self.restaurant.restaurant_name} with value {self.total_value}"

class OrderItem(models.Model):
    """
    Model for order items.

    Attributes:
        order (Order): The order to which this item belongs.
        menu_item (Menu): The menu item for the order item.
        quantity (int): The quantity of the menu item in the order.
    """

    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        """
        Returns a string representation of the order item.

        Returns:
            str: String representation of the order item.
        """
        return f"Order {self.order.id} - {self.quantity} {self.menu_item.item}(s)"

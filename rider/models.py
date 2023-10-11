from django.db import models
from accounts.models import User
from orders.models import Order
from django.db.models.functions import ACos, Cos, Radians, Sin
from django.db.models import F, FloatField
from django.db.models.functions import Cast

class Rider(models.Model):
    """
    Model representing a rider.

    Attributes:
        rider (User): The associated user representing the rider.
        order (Order): The associated order.
        latitude (Decimal): The latitude of the rider's location.
        longitude (Decimal): The longitude of the rider's location.
        is_picked_up (bool): A flag indicating if the rider has been picked up for an order.
        is_delivered (bool): A flag indicating if the order has been delivered to the rider.
    """

    rider = models.OneToOneField(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    is_picked_up = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)

    def __str__(self):
        """
        String representation of the rider.

        Returns:
            str: The string representation of the rider.
        """
        return str(self.rider)

    @classmethod
    def get_riders_within_range(cls, restaurant_latitude, restaurant_longitude, distance_range):
        """
        Gets riders within a specified distance range from a restaurant.

        Args:
            restaurant_latitude (float): The latitude of the restaurant.
            restaurant_longitude (float): The longitude of the restaurant.
            distance_range (float): The distance range in kilometers.

        Returns:
            QuerySet: Queryset of riders within the specified distance range.
        """
        return cls.objects.annotate(
            distance=Cast(
                6371 * ACos(
                    Cos(Radians(restaurant_latitude)) * Cos(Radians(F('latitude'))) *
                    Cos(Radians(F('longitude')) - Radians(restaurant_longitude)) +
                    Sin(Radians(restaurant_latitude)) * Sin(Radians(F('latitude')))
                ),
                output_field=FloatField()
            )
        ).filter(distance__lte=distance_range, is_picked_up=False).order_by('distance')

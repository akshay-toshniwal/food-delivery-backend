from django.db import models
from accounts.models import User

class Cuisine(models.Model):
    """
    Model for cuisine.

    Attributes:
        name (str): The name of the cuisine.
    """

    name = models.CharField(max_length=100)

    def __str__(self):
        """
        Returns a string representation of the cuisine.

        Returns:
            str: The name of the cuisine.
        """
        return self.name

class Restaurant(models.Model):
    """
    Model for a restaurant.

    Attributes:
        restaurant_manager (User): The manager of the restaurant.
        restaurant_name (str): The name of the restaurant.
        restaurant_phone (str): The phone number of the restaurant.
        restaurant_status (int): The status of the restaurant (choices defined in RESTAURANT_STATUS).
        cuisines (list): The cuisines offered by the restaurant.
        opening_time (Time): The opening time of the restaurant.
        closing_time (Time): The closing time of the restaurant.
        restaurant_address (str): The address of the restaurant.
        restaurant_state (str): The state where the restaurant is located.
        restaurant_city (str): The city where the restaurant is located.
        restaurant_pin_code (str): The pin code of the restaurant's location.
        latitude (float): The latitude of the restaurant's location.
        longitude (float): The longitude of the restaurant's location.
    """

    OPENED = 1
    CLOSED = 2

    RESTAURANT_STATUS = (
        (OPENED, 'Opened'),
        (CLOSED, 'Closed'),
    )

    class Meta:
        verbose_name = 'restaurant'
        verbose_name_plural = 'restaurants'

    restaurant_manager = models.OneToOneField(User, on_delete=models.CASCADE)
    restaurant_name = models.CharField(max_length=30, blank=False)
    restaurant_phone = models.CharField(max_length=10, null=False, blank=False)
    restaurant_status = models.PositiveSmallIntegerField(choices=RESTAURANT_STATUS, default=1)
    cuisines = models.ManyToManyField(Cuisine, blank=True)
    opening_time = models.TimeField()
    closing_time = models.TimeField()

    restaurant_address = models.CharField(max_length=250, blank=True, null=True)
    restaurant_state = models.CharField(max_length=15, blank=True, null=True)
    restaurant_city = models.CharField(max_length=15, blank=True, null=True)
    restaurant_pin_code = models.CharField(max_length=6, blank=True, null=True)

    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        """
        Returns a string representation of the restaurant.

        Returns:
            str: The name of the restaurant.
        """
        return self.restaurant_name

class Menu(models.Model):
    """
    Model for a menu item.

    Attributes:
        restaurant (Restaurant): The restaurant to which this menu item belongs.
        item (str): The name of the menu item.
        price (int): The price of the menu item.
    """

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    item = models.CharField(max_length=30)
    price = models.PositiveSmallIntegerField()

    def __str__(self):
        """
        Returns a string representation of the menu item.

        Returns:
            str: The name of the menu item.
        """
        return self.item

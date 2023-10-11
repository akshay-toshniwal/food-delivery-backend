from rest_framework import serializers
from .models import Restaurant, Cuisine, Menu
from rider.serializers import NearestRiderSerializer

class CuisineSerializer(serializers.ModelSerializer):
    """Serializer for Cuisine model."""

    class Meta:
        model = Cuisine
        fields = '__all__'

class MenuSerializer(serializers.ModelSerializer):
    """
    Serializer for Menu model.

    Args:
        included_fields (list): A list of fields to include.

    Attributes:
        Meta (class): Metadata options for the serializer.

    Methods:
        __init__: Initializes the MenuSerializer instance.

    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the MenuSerializer instance.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        """

        # Get the fields to include from kwargs or default to including all fields
        included_fields = kwargs.pop('included_fields', None)
        super(MenuSerializer, self).__init__(*args, **kwargs)

        if included_fields:
            # Drop fields that are not in the included fields list
            allowed = set(included_fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = Menu
        fields = '__all__'


class RestaurantSerializer(serializers.ModelSerializer):
    """
    Serializer for Restaurant model.

    Attributes:
        cuisines (CuisineSerializer): Serializer for related cuisines.
        menu (MenuSerializer): Serializer for related menu items.

    """
    
    cuisines = CuisineSerializer(many=True, required=False)
    menu = MenuSerializer(many=True, required=False)

    class Meta:
        model = Restaurant
        fields = '__all__'

    def create(self, validated_data):
        """
        Create a new restaurant instance.

        Args:
            validated_data (dict): Validated data for creating the restaurant.

        Returns:
            Restaurant: The newly created restaurant instance.

        """

        cuisines_data = validated_data.pop('cuisines', [])
        menu_data = validated_data.pop('menu', [])

        restaurant = Restaurant.objects.create(**validated_data)

        # Handle cuisines if provided
        for cuisine_data in cuisines_data:
            cuisine, created = Cuisine.objects.get_or_create(**cuisine_data)
            restaurant.cuisines.add(cuisine)

        # Handle menu items if provided
        for menu_item_data in menu_data:
            Menu.objects.create(restaurant=restaurant, **menu_item_data)

        return restaurant
    
    def update(self, instance, validated_data):
        """
        Update an existing restaurant instance.

        Args:
            instance (Restaurant): The existing restaurant instance to update.
            validated_data (dict): Validated data for updating the restaurant.

        Returns:
            Restaurant: The updated restaurant instance.

        """
        
        instance.restaurant_name = validated_data.get('restaurant_name', instance.restaurant_name)
        instance.restaurant_phone = validated_data.get('restaurant_phone', instance.restaurant_phone)
        instance.opening_time = validated_data.get('opening_time', instance.opening_time)
        instance.closing_time = validated_data.get('closing_time', instance.closing_time)
        instance.restaurant_address = validated_data.get('restaurant_address', instance.restaurant_address)
        instance.restaurant_state = validated_data.get('restaurant_state', instance.restaurant_state)
        instance.restaurant_city = validated_data.get('restaurant_city', instance.restaurant_city)
        instance.restaurant_pin_code = validated_data.get('restaurant_pin_code', instance.restaurant_pin_code)
        instance.latitude = validated_data.get('latitude', instance.latitude)
        instance.longitude = validated_data.get('longitude', instance.longitude)

        cuisines_data = validated_data.get('cuisines', [])
        menu_data = validated_data.get('menu', [])
        
        # Handle cuisines update and addition
        instance.cuisines.clear()
        for cuisine_data in cuisines_data:
            cuisine, created = Cuisine.objects.get_or_create(**cuisine_data)
            instance.cuisines.add(cuisine)

        # Handle menu items update
        Menu.objects.filter(restaurant=instance).delete()
        for menu_item_data in menu_data:
            Menu.objects.create(restaurant=instance, **menu_item_data)

        instance.save()
        return instance


class RestaurantSuggestionSerializer(serializers.Serializer):
    """
    Serializer for restaurant suggestions.

    Args:
        kind_of_food (str): The kind of food desired.
        desired_time (datetime.time): The desired time for the suggestion.

    Attributes:
        kind_of_food (str): The kind of food desired.
        desired_time (datetime.time): The desired time for the suggestion.

    """

    kind_of_food = serializers.CharField()
    desired_time = serializers.TimeField()



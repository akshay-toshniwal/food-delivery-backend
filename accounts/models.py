import uuid
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from .managers import CustomUserManager

class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model.

    This model extends AbstractBaseUser and PermissionsMixin to customize user behavior.

    Attributes:
        uid (UUID): Public identifier for the user.
        email (str): Email address of the user (unique).
        first_name (str): First name of the user.
        last_name (str): Last name of the user.
        phone (str): Phone number of the user.
        role (int): User's role (choices defined in ROLE_CHOICES).
        address (str): User's address.
        country (str): User's country.
        state (str): User's state.
        city (str): User's city.
        pin_code (str): User's pin code.
        is_active (bool): Indicates if the user is active.
        is_deleted (bool): Indicates if the user is deleted.
        created_date (datetime): Date and time when the user was created.
        modified_date (datetime): Date and time when the user was last modified.
        is_staff (bool): Indicates if the user is staff.
    """

    ADMIN = 1
    USER = 2
    RESTAURANT = 3
    RIDER = 4

    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (USER, 'User'),
        (RESTAURANT, 'Restaurant'),
        (RIDER, 'Rider'),
    )

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    uid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, verbose_name='Public identifier')
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=10, null=False, blank=False)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=3)

    address = models.CharField(max_length=250, blank=True, null=True)
    country = models.CharField(max_length=15, blank=True, null=True)
    state = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=15, blank=True, null=True)
    pin_code = models.CharField(max_length=6, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        """
        Returns a string representation of the user.

        Returns:
            str: Email address of the user.
        """
        return self.email
    
    @property
    def get_full_name(self):
        """
        Returns the full name of the user.

        Returns:
            str: Full name in the format "first_name last_name".
        """
        return self.first_name + " " + self.last_name

from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    Attributes:
        email (str): Email address of the user.
        password (str): User's password.
        first_name (str): User's first name.
        last_name (str): User's last name.
        role (int): User's role.
    """

    class Meta:
        model = User
        fields = (
            'email',
            'password',
            'first_name',
            'last_name',
            'role'
        )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        Creates a new user.

        Args:
            validated_data (dict): Validated user data.

        Returns:
            User: The newly created user.
        """
        auth_user = User.objects.create_user(**validated_data)
        return auth_user

class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login.

    Attributes:
        email (str): Email address of the user.
        password (str): User's password.
        access (str): Access token.
        refresh (str): Refresh token.
        role (str): User's role.
        full_name (str): User's full name.
    """

    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    role = serializers.CharField(read_only=True)
    full_name = serializers.CharField(read_only=True)

    def validate(self, data):
        """
        Validates user login credentials.

        Args:
            data (dict): Input data containing email and password.

        Returns:
            dict: Validated user login information.
        """
        email = data['email']
        password = data['password']
        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid login credentials")

        try:
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh)
            access_token = str(refresh.access_token)

            update_last_login(None, user)

            validation = {
                'access': access_token,
                'refresh': refresh_token,
                'email': user.email,
                'full_name': user.get_full_name,
                'role': user.role,
            }
            return validation
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid login credentials")

class UserListSerializer(serializers.ModelSerializer):
    """
    Serializer for user listing.

    Attributes:
        email (str): Email address of the user.
        role (int): User's role.
    """

    class Meta:
        model = User
        fields = ('email','role')

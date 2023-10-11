from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from permissions import IsAdminRole
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserListSerializer
from .models import User


class UserRegistrationView(APIView):
    """
    API view for user registration.
    """

    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        """
        Handles user registration.

        Args:
            request (Request): HTTP request.

        Returns:
            Response: HTTP response with registration information.
        """
        data = request.data.copy()
        data["role"] = User.USER
        serializer = self.serializer_class(data=data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            serializer.save()
            status_code = status.HTTP_201_CREATED

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User successfully registered!',
                'user': serializer.data
            }

            return Response(response, status=status_code)

class RiderRegistrationView(APIView):
    """
    API view for rider registration.
    """

    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        """
        Handles rider registration.

        Args:
            request (Request): HTTP request.

        Returns:
            Response: HTTP response with registration information for a rider.
        """
        data = request.data.copy()
        data["role"] = User.RIDER
        serializer = self.serializer_class(data=data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            serializer.save()
            status_code = status.HTTP_201_CREATED

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'Rider successfully registered!',
                'user': serializer.data
            }

            return Response(response, status=status_code)

class RestaurantRegistrationView(APIView):
    """
    API view for restaurant registration.
    """

    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        """
        Handles restaurant manager registration.

        Args:
            request (Request): HTTP request.

        Returns:
            Response: HTTP response with registration information for a restaurant manager.
        """
        data = request.data.copy()
        data["role"] = User.RESTAURANT
        serializer = self.serializer_class(data=data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            serializer.save()
            status_code = status.HTTP_201_CREATED

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'Restaurant Manager successfully registered!',
                'user': serializer.data
            }

            return Response(response, status=status_code)

class UserLoginView(APIView):
    """
    API view for user login.
    """

    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        """
        Handles user login.

        Args:
            request (Request): HTTP request.

        Returns:
            Response: HTTP response with login information.
        """
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            status_code = status.HTTP_200_OK

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User logged in successfully',
                'access': serializer.data['access'],
                'refresh': serializer.data['refresh'],
                'authenticatedUser': {
                    'email': serializer.data['email'],
                    'role': serializer.data['role'],
                    'name': serializer.data['full_name']
                }
            }

            return Response(response, status=status_code)

class UserListView(APIView):
    """
    API view for listing users.
    """

    serializer_class = UserListSerializer
    permission_classes = (IsAuthenticated, IsAdminRole)

    def get(self, request):
        """
        Gets a list of users.

        Args:
            request (Request): HTTP request.

        Returns:
            Response: HTTP response with user listing information.
        """
        users = User.objects.all()
        serializer = self.serializer_class(users, many=True)
        response = {
            'success': True,
            'status_code': status.HTTP_200_OK,
            'message': 'Successfully fetched users',
            'users': serializer.data
        }

        return Response(response, status=status.HTTP_200_OK)

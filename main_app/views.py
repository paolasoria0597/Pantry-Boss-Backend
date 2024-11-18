from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail, BadHeaderError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

# Import our models and serializers
from .models import Floor, Pantry, Dispenser
from django.contrib.auth.models import User
from .serializers import FloorSerializer, PantrySerializer, DispenserSerializer, UserSerializer, LoginSerializer


# --------------------------------------------------------
# FLOOR VIEWS
# --------------------------------------------------------

# This view handles listing all floors and creating new floors
class FloorListCreateView(generics.ListCreateAPIView):
    """
    Handles:
    - GET: List all floors
    - POST: Create a new floor
    """
    queryset = Floor.objects.all()
    serializer_class = FloorSerializer


# This view handles retrieving, updating, or deleting a specific floor by ID
class FloorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Handles:
    - GET: Retrieve a specific floor by ID
    - PUT: Update a specific floor by ID
    - DELETE: Delete a specific floor by ID
    """
    queryset = Floor.objects.all()
    serializer_class = FloorSerializer
    lookup_field = 'id'  # Use 'id' instead of the default 'pk'


# --------------------------------------------------------
# PANTRY VIEWS
# --------------------------------------------------------

# Handles listing all pantries and creating new ones
class PantryListCreateView(generics.ListCreateAPIView):
    """
    Handles:
    - GET: List all pantries
    - POST: Create a new pantry
    """
    queryset = Pantry.objects.all()
    serializer_class = PantrySerializer


# Handles retrieving, updating, or deleting a specific pantry by ID
class PantryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Handles:
    - GET: Retrieve a specific pantry by ID
    - PUT: Update a specific pantry by ID
    - DELETE: Delete a specific pantry by ID
    """
    queryset = Pantry.objects.all()
    serializer_class = PantrySerializer
    lookup_field = 'id'


# --------------------------------------------------------
# DISPENSER VIEWS
# --------------------------------------------------------

# Handles listing all dispensers and creating new ones
class DispenserListCreateView(generics.ListCreateAPIView):
    """
    Handles:
    - GET: List all dispensers
    - POST: Create a new dispenser
    """
    queryset = Dispenser.objects.all()
    serializer_class = DispenserSerializer


# Handles retrieving, updating, or deleting a specific dispenser by ID
class DispenserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Handles:
    - GET: Retrieve a specific dispenser by ID
    - PUT: Update a specific dispenser by ID
    - DELETE: Delete a specific dispenser by ID
    """
    queryset = Dispenser.objects.all()
    serializer_class = DispenserSerializer
    lookup_field = 'id'


# --------------------------------------------------------
# CUSTOM API VIEW FOR UPDATING DISPENSER LEVEL
# --------------------------------------------------------

class UpdateDispenserLevel(APIView):
    """
    Handles:
    - POST: Update the level of a dispenser and notify if it's running low
    """

    @swagger_auto_schema(
        operation_description="Update the current level of a dispenser",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'current_level': openapi.Schema(type=openapi.TYPE_INTEGER, description='Current level in units'),
            },
            required=['current_level']
        ),
        responses={
            200: "Dispenser updated successfully",
            404: "Dispenser not found",
            400: "Invalid data",
        }
    )
    def post(self, request, id):
        # Try to get the dispenser with the given ID
        try:
            dispenser = Dispenser.objects.get(id=id)
        except Dispenser.DoesNotExist:
            return Response({"error": "Dispenser not found"}, status=status.HTTP_404_NOT_FOUND)

        # Get the 'current_level' from the request data
        new_level = request.data.get('current_level')
        if new_level is None:
            return Response({"error": "'current_level' is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure the new level is an integer and is not negative
        try:
            new_level = int(new_level)
            if new_level < 0:
                raise ValueError("Level cannot be negative")
        except ValueError:
            return Response({"error": "'current_level' must be a positive integer"}, status=status.HTTP_400_BAD_REQUEST)

        # Update the dispenser's current level
        dispenser.current_level = new_level
        dispenser.save()

        # Check if the dispenser is running low and send a notification
        if dispenser.is_running_low():
            self.notify_user(dispenser)

        return Response({"message": "Dispenser updated successfully"}, status=status.HTTP_200_OK)

    def notify_user(self, dispenser):
        """
        Sends an email notification if the dispenser level is too low.
        """
        subject = f"{dispenser.get_type_display()} Dispenser Running Low"
        message = (
            f"The dispenser in pantry '{dispenser.pantry.name}' on floor '{dispenser.pantry.floor.number}' "
            "is running low. Please refill it soon."
        )
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email='no-reply@yourapp.com',
                recipient_list=['user@example.com']
            )
        except BadHeaderError:
            print("Invalid email header detected.")
        except Exception as e:
            print(f"Failed to send email: {e}")

# --------------------------------------------------------
# CUSTOM API VIEW FOR AUTH
# --------------------------------------------------------

# **User Registration View**
class CreateUserView(generics.CreateAPIView):
    """
    Allows new users to register.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        # Call the parent class's create method
        response = super().create(request, *args, **kwargs)

        # Fetch the newly created user based on the response data
        user = User.objects.get(username=response.data['username'])

        # Generate a refresh token for the new user
        refresh = RefreshToken.for_user(user)

        # Return the response with the tokens and user data
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': response.data
        }, status=status.HTTP_201_CREATED)



# login view
class LoginView(APIView):
    """
    Authenticates a user and returns a JWT token.
    """
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Authenticate user and get access/refresh tokens",
        request_body=LoginSerializer,
        responses={
            200: "Authentication successful",
            401: "Invalid credentials"
        }
    )
    def post(self, request, *args, **kwargs):
        # Use the LoginSerializer to validate input
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        # Authenticate the user
        user = authenticate(username=username, password=password)
        if user is not None:
            # Generate a refresh token for the authenticated user
            refresh = RefreshToken.for_user(user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)

        # Return an error response if authentication fails
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


# **User Verification View**
class VerifyUserView(APIView):
    """
    Verifies if the user is authenticated and provides a new set of tokens.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Fetch the authenticated user
        user = request.user

        # Generate a new refresh token for the authenticated user
        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        }, status=status.HTTP_200_OK)
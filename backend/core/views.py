import logging
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Item, Book
from .serializers import ItemSerializer, BookSerializer

logger = logging.getLogger('api.auth')

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = []  # Disable authentication for login
    """
    API endpoint for user login with logging.
    """
    def options(self, request, *args, **kwargs):
        response = Response()
        response["Allow"] = "POST, OPTIONS"
        response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type"
        return response
    def post(self, request):
        logger.info(f'Received request data: {request.data}')
        logger.info(f'Request content type: {request.content_type}')
        username = request.data.get('username')
        password = request.data.get('password')
        
        logger.info(f'Extracted username: {username}, password received: {bool(password)}')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                token, _ = Token.objects.get_or_create(user=user)
                logger.info(f'Successful login for user: {username}')
                # Get user groups/roles
                groups = [group.name for group in user.groups.all()]
                return Response({
                    'token': token.key,
                    'message': 'Login successful',
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'is_staff': user.is_staff,
                        'is_superuser': user.is_superuser,
                        'groups': groups
                    }
                })
            else:
                logger.warning(f'Failed login attempt for user: {username}')
                return Response({
                    'error': 'Invalid credentials'
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            logger.warning('Login attempt with missing credentials')
            return Response({
                'error': 'Please provide both username and password'
            }, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class UserInfoView(APIView):
    permission_classes = (IsAuthenticated,)
    """
    API endpoint to get current user information
    """
    def options(self, request, *args, **kwargs):
        response = Response()
        response["Allow"] = "GET, OPTIONS"
        response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Authorization, Content-Type"
        return response

    def get(self, request):
        user = request.user
        groups = [group.name for group in user.groups.all()]
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
            'groups': groups
        })

class ItemViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Item instances.
    Only authenticated users can access these endpoints.
    """
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

class BookViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Book instances.
    Only authenticated users can access these endpoints.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
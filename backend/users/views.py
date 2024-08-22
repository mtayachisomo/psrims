# users/views.py

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from django.db.models.functions import Lower
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from .models import User, Role, UserRole, Permission, RolePermission, Position, UserPosition
from .permissions import Security  # Import the Security class
from institutions.models import InstitutionUser
from .serializers import (
    UserCreateSerializer, UserUpdateSerializer, UserSerializer, 
    UserLoginSerializer, LogoutSerializer, PasswordChangeSerializer, 
    PasswordResetSerializer, PasswordResetConfirmSerializer,
    RoleCreateSerializer, RoleUpdateSerializer, RoleSerializer,
    UserRoleSerializer, UserRoleCreateSerializer, UserRoleDetailSerializer, PermissionSerializer,
    RolePermissionSerializer, PositionSerializer, PositionCreateSerializer, PositionSerializer, UserPositionSerializer, 
    UserPositionCreateSerializer, UserDetailSerializer
)

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user_id = self.request.user.id
        security = Security()
        # Use the correct permission code here
        security.secureAccess('create_user', user_id)
        serializer.save()   


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'  # Change 'limit' to control the number of items per page

class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination  # Use the custom pagination class

    def get_queryset(self):
        # Retrieve query parameters for pagination, skip, limit, and search
        skip = self.request.query_params.get('skip', 0)
        limit = self.request.query_params.get('limit', 10)
        search = self.request.query_params.get('search', '')

        # Ensure that skip and limit are integers
        try:
            skip = int(skip)
            limit = int(limit)
        except ValueError:
            skip = 0
            limit = 10

        # Retrieve the user ID
        user_id = self.request.user.id

        # Secure access
        security = Security()
        security.secureAccess('create_user', user_id)

        # Perform filtering and searching
        queryset = User.objects.filter(deleted=False)
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) | 
                Q(last_name__icontains=search) | 
                Q(email__icontains=search)
            )

        # Order queryset by the alphabetical order of the first letter of the first_name field
        queryset = queryset.annotate(first_name_lower=Lower('first_name')).order_by('first_name_lower')

        # Apply pagination and return the queryset
        return queryset[skip: skip + limit]


class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.id
        security = Security()
        security.secureAccess('create_user', user_id)
        return User.objects.filter(deleted=False)

class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        user_id = self.request.user.id
        security = Security()
        security.secureAccess('create_user', user_id)
        serializer.save()

class UserDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        user_id = self.request.user.id
        security = Security()
        security.secureAccess('create_user', user_id)
        user = get_object_or_404(User, pk=pk)
        user.deleted = True
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class DeletedUserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.id
        security = Security()
        security.secureAccess('create_user', user_id)
        return User.objects.filter(deleted=True)

class UserLoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        tokens = serializer.validated_data['tokens']
        return Response({'email': user.email, 'tokens': tokens}, status=status.HTTP_200_OK)
    
class CurrentUserView(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        # Retrieve the InstitutionUser instances related to the current user
        institution_users = InstitutionUser.objects.filter(user=user)
        # Retrieve the related institutions from the InstitutionUser instances
        institutions = [institution_user.institution for institution_user in institution_users]
        # Add institutions to the user instance
        user.institutions = institutions
        return user

class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request):
        refresh_token = None
        
        # Option 1: Extract refresh token from request headers
        authorization_header = request.headers.get('Authorization')
        if authorization_header and authorization_header.startswith('Bearer '):
            refresh_token = authorization_header.split(' ')[1]

        # Option 2: Extract refresh token from request cookies
        # refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            return Response({"refresh_token": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data={'refresh_token': refresh_token})

        if serializer.is_valid():
            # Perform logout actions here
            return Response({"message": "User successfully logged out."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PasswordChangeSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Password changed successfully."})

class PasswordResetView(APIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Password reset instructions have been sent to your email."})

class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                user.set_password(serializer.validated_data['new_password'])
                user.save()
                return Response({"message": "Password has been reset."})
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Invalid token or user ID."}, status=status.HTTP_400_BAD_REQUEST)


class RoleCreateView(generics.CreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user_id = self.request.user.id
        security = Security()
        security.secureAccess('create_user', user_id)
        serializer.save()

class RoleListView(generics.ListAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        skip = self.request.query_params.get('skip', 0)
        limit = self.request.query_params.get('limit', 10)
        search = self.request.query_params.get('search', '')

        try:
            skip = int(skip)
            limit = int(limit)
        except ValueError:
            skip = 0
            limit = 10
            
        # Retrieve the user ID
        user_id = self.request.user.id

        # Secure access
        security = Security()
        security.secureAccess('create_user', user_id)

        queryset = super().get_queryset()

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search)
            )

        queryset = queryset.annotate(name_lower=Lower('name')).order_by('name_lower')

        return queryset[skip: skip + limit]

class RoleDetailView(generics.RetrieveAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.id
        security = Security()
        security.secureAccess('create_user', user_id)
        return super().get_queryset()

class RoleUpdateView(generics.UpdateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        user_id = self.request.user.id
        security = Security()
        security.secureAccess('create_user', user_id)
        serializer.save()

class RoleDeleteView(generics.DestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        user_id = self.request.user.id
        security = Security()
        security.secureAccess('create_user', user_id)
        instance.delete()

class UserRoleCreateView(generics.CreateAPIView):
    queryset = UserRole.objects.all()
    serializer_class = UserRoleCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user_id = self.request.user.id
        security = Security()
        security.secureAccess('create_user', user_id)
        serializer.save()

class UserRoleListView(generics.ListAPIView):
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.id
        security = Security()
        security.secureAccess('create_user', user_id)
        return super().get_queryset()

class UserRoleDetailView(generics.RetrieveAPIView):
    queryset = UserRole.objects.all()
    serializer_class = UserRoleDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.id
        security = Security()
        security.secureAccess('create_user', user_id)
        return super().get_queryset()

class UserRoleUpdateView(generics.UpdateAPIView):
    queryset = UserRole.objects.all()
    serializer_class = UserRoleCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        user_id = self.request.user.id
        security = Security()
        security.secureAccess('create_user', user_id)
        serializer.save()

class UserRoleDeleteView(generics.DestroyAPIView):
    queryset = UserRole.objects.all()
    serializer_class = UserRoleDetailSerializer
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        user_id = self.request.user.id
        security = Security()
        security.secureAccess('create_user', user_id)
        instance.delete()

class PermissionCreateView(generics.CreateAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user_id = self.request.user.id
        security = Security()
        security.secureAccess('create_user', user_id)
        serializer.save()

class PermissionDetailView(generics.RetrieveAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.id
        security = Security()
        security.secureAccess('create_user', user_id)
        return super().get_queryset()
        
class PermissionUpdateView(generics.UpdateAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        user_id = self.request.user.id
        security = Security()
        security.secureAccess('create_user', user_id)
        serializer.save()
        
class PermissionDeleteView(generics.DestroyAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        user_id = self.request.user.id
        security = Security()
        security.secureAccess('create_user', user_id)
        instance.delete()


class PermissionListView(generics.ListCreateAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        skip = self.request.query_params.get('skip', 0)
        limit = self.request.query_params.get('limit', 10)
        search = self.request.query_params.get('search', '')

        try:
            skip = int(skip)
            limit = int(limit)
        except ValueError:
            skip = 0
            limit = 10

        user_id = self.request.user.id

        # Assuming 'create_user' is a permission associated with users
        security = Security()
        security.secureAccess('create_user', user_id)

        queryset = Permission.objects.all()

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(content_type__app_label__icontains=search) |
                Q(content_type__model__icontains=search)
            )

        queryset = queryset.order_by('id')
        
        return queryset[skip: skip + limit]

        
class RolePermissionCreateView(generics.CreateAPIView):
    queryset = RolePermission.objects.all()
    serializer_class = RolePermissionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user_id = self.request.user.id
        security = Security()
        security.secureAccess('create_user', user_id)
        serializer.save()
        
class RolePermissionListView(generics.ListCreateAPIView):
    queryset = RolePermission.objects.all()
    serializer_class = RolePermissionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.id
        security = Security()
        security.secureAccess('create_user', user_id)
        return super().get_queryset()
    
class RolePermissionUpdateView(generics.UpdateAPIView):
    queryset = Permission.objects.all()
    serializer_class = RolePermissionSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        user_id = self.request.user.id
        security = Security()
        security.secureAccess('create_user', user_id)
        serializer.save()

class RolePermissionDetailView(generics.RetrieveAPIView):
    queryset = RolePermission.objects.all()
    serializer_class = RolePermissionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.id
        security = Security()
        security.secureAccess('create_user', user_id)
        return super().get_queryset()

class RolePermissionDeleteView(generics.DestroyAPIView):
    queryset = RolePermission.objects.all()
    serializer_class = RolePermissionSerializer
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        user_id = self.request.user.id
        security = Security()
        security.secureAccess('create_user', user_id)
        instance.delete()

class PositionCreateView(generics.CreateAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user_id = self.request.user.id
        security = Security()
        security.secureAccess('create_user', user_id)
        serializer.save()

class PositionListView(generics.ListAPIView):
    serializer_class = PositionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        user_id = self.request.user.id
        security = Security()  # Assuming Security is defined in users.models
        security.secureAccess('list_positions', user_id)

        skip = self.request.query_params.get('skip', 0)
        limit = self.request.query_params.get('limit', 10)
        search = self.request.query_params.get('search', '')

        try:
            skip = int(skip)
            limit = int(limit)
        except ValueError:
            skip = 0
            limit = 10
            
        user_id = self.request.user.id

        # Assuming 'create_user' is a permission associated with users
        security = Security()
        security.secureAccess('create_user', user_id)

        queryset = Position.objects.filter(deleted=False)

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search)
            )

        queryset = queryset.annotate(name_lower=Lower('name')).order_by('name_lower')

        return queryset[skip: skip + limit]


class PositionDetailView(generics.RetrieveAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.id
        security = Security()
        security.secureAccess('create_user', user_id)
        return super().get_queryset()

class PositionUpdateView(generics.UpdateAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        user_id = self.request.user.id
        security = Security()
        security.secureAccess('create_user', user_id)
        serializer.save()

class PositionDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        user_id = self.request.user.id
        security = Security()
        security.secureAccess('create_user', user_id)
        position = get_object_or_404(Position, pk=pk)
        position.deleted = True
        position.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserPositionCreateView(generics.CreateAPIView):
    queryset = UserPosition.objects.all()
    serializer_class = UserPositionCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user_id = self.request.user.id
        security = Security()
        security.secureAccess('create_user', user_id)
        serializer.save()

class UserPositionListView(generics.ListAPIView):
    queryset = UserPosition.objects.all()
    serializer_class = UserPositionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.id
        security = Security()
        security.secureAccess('create_user', user_id)
        return super().get_queryset()

class UserPositionDetailView(generics.RetrieveAPIView):
    queryset = UserPosition.objects.all()
    serializer_class = UserPositionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.id
        security = Security()
        security.secureAccess('create_user', user_id)
        return super().get_queryset()

class UserPositionUpdateView(generics.UpdateAPIView):
    queryset = UserPosition.objects.all()
    serializer_class = UserPositionCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        user_id = self.request.user.id
        security = Security()
        security.secureAccess('create_user', user_id)
        serializer.save()

class UserPositionDeleteView(generics.DestroyAPIView):
    queryset = UserPosition.objects.all()
    serializer_class = UserPositionSerializer
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        user_id = self.request.user.id
        security = Security()
        security.secureAccess('create_user', user_id)
        instance.delete()
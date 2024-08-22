# users/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('users/me/', views.CurrentUserView.as_view(), name='current-user'),
    path('users/', views.UserListView.as_view(), name='user-list'),          # Read All
    path('users/create/', views.UserCreateView.as_view(), name='user-create'), # Create
    path('users/<uuid:pk>/', views.UserDetailView.as_view(), name='user-detail'), # Read One
    path('users/update/<uuid:pk>/', views.UserUpdateView.as_view(), name='user-update'), # Update
    path('users/delete/<uuid:pk>/', views.UserDeleteView.as_view(), name='user-delete'), # Show Delete Confirmation and Handle Deletion
    path('users/deleted/', views.DeletedUserListView.as_view(), name='deleted-user-list'), # List Deleted Users
    path('users/login/', views.UserLoginView.as_view(), name='user-login'), # Login
    path('users/logout/', views.UserLogoutView.as_view(), name='user-logout'),  # Logout
    path('users/password-change/', views.PasswordChangeView.as_view(), name='password-change'), # Password Change
    path('users/password-reset/', views.PasswordResetView.as_view(), name='password-reset'),
    path('users/password-reset-confirm/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password-reset-confirm'),

    # Role endpoints
    path('roles/', views.RoleListView.as_view(), name='role-list'),          # Read All Roles
    path('roles/create/', views.RoleCreateView.as_view(), name='role-create'), # Create Role
    path('roles/<int:pk>/', views.RoleDetailView.as_view(), name='role-detail'), # Read One Role
    path('roles/update/<int:pk>/', views.RoleUpdateView.as_view(), name='role-update'), # Update Role
    path('roles/delete/<int:pk>/', views.RoleDeleteView.as_view(), name='role-delete'), # Delete Role

    # UserRole endpoints
    path('user-roles/', views.UserRoleListView.as_view(), name='user-role-list'),          # Read All UserRoles
    path('user-roles/create/', views.UserRoleCreateView.as_view(), name='user-role-create'), # Create UserRole
    path('user-roles/<int:pk>/', views.UserRoleDetailView.as_view(), name='user-role-detail'), # Read One UserRole
    path('user-roles/update/<int:pk>/', views.UserRoleUpdateView.as_view(), name='user-role-update'), # Update UserRole
    path('user-roles/delete/<int:pk>/', views.UserRoleDeleteView.as_view(), name='user-role-delete'), # Delete UserRole
    
    # Permission endpoints
    path('permissions/', views.PermissionListView.as_view(), name='permission-list'),          # Read All Permissions
    path('permissions/create/', views.PermissionCreateView.as_view(), name='permission-create'), # Create Permission
    path('permissions/<int:pk>/', views.PermissionDetailView.as_view(), name='permission-detail'), # Read One Permission
    path('permissions/update/<int:pk>/', views.PermissionUpdateView.as_view(), name='permission-update'), # Update Permission
    path('permissions/delete/<int:pk>/', views.PermissionDeleteView.as_view(), name='permission-delete'), # Delete Permission

    # RolePermission endpoints
    path('role-permissions/', views.RolePermissionListView.as_view(), name='role-permission-list'),          # Read All RolePermissions
    path('role-permissions/create/', views.RolePermissionCreateView.as_view(), name='role-permission-create'), # Create RolePermission
    path('role-permissions/<int:pk>/', views.RolePermissionDetailView.as_view(), name='role-permission-detail'), # Read One RolePermission
    path('role-permissions/update/<int:pk>/', views.RolePermissionUpdateView.as_view(), name='role-permission-update'), # Update RolePermission
    path('role-permissions/delete/<int:pk>/', views.RolePermissionDeleteView.as_view(), name='role-permission-delete'), # Delete RolePermission
    
    # Position endpoints
    path('positions/', views.PositionListView.as_view(), name='position-list'),          # Read All Positions
    path('positions/create/', views.PositionCreateView.as_view(), name='position-create'), # Create Position
    path('positions/<int:pk>/', views.PositionDetailView.as_view(), name='position-detail'), # Read One Position
    path('positions/update/<int:pk>/', views.PositionUpdateView.as_view(), name='position-update'), # Update Position
    path('positions/delete/<int:pk>/', views.PositionDeleteView.as_view(), name='position-delete'), # Delete Position
    
    # UserPosition endpoints
    path('user-positions/', views.UserPositionListView.as_view(), name='user-position-list'),
    path('user-positions/create/', views.UserPositionCreateView.as_view(), name='user-position-create'),
    path('user-positions/<int:pk>/', views.UserPositionDetailView.as_view(), name='user-position-detail'),
    path('user-positions/update/<int:pk>/', views.UserPositionUpdateView.as_view(), name='user-position-update'),
    path('user-positions/delete/<int:pk>/', views.UserPositionDeleteView.as_view(), name='user-position-delete'),



]

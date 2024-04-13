from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Role, ActionType, Resource, UserRole
from .utils import assign_role_to_user,remove_user_role
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
    

def assign_role(request):
    if request.method == 'POST':
        username = request.POST.get('user')
        roles = request.POST.getlist('roles')
        users = User.objects.all()

        # Check if username is provided
        if not username:
            return render(request, 'assign_role.html', {'error_message': 'Please select a user.', 'users': users})

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return render(request, 'assign_role.html', {'error_message': 'User does not exist.', 'users': users})

        # Assign roles to user
        for role_name in roles:
            try:
                role, created = Role.objects.get_or_create(name=role_name)
                if not UserRole.objects.filter(user=user, role=role).exists():
                    assign_role_to_user(user, role)
            except Role.DoesNotExist:
                return render(request, 'assign_role.html', {'error_message': f'Role "{role_name}" does not exist.', 'users': users})

    users = User.objects.all()
    return render(request, 'assign_role.html', {'users': users})



def create_user_with_roles(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        roles = request.POST.getlist('roles')
        
        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            return render(request, 'create_user_with_roles.html', {'roles': Role.objects.all(), 'error_message': 'Username already exists'})
        
        try:
            # Create the user
            user = User.objects.create_user(username=username, password=password)
            
            # Assign roles to the user
            for role_name in roles:
                try:
                    role = Role.objects.get(name=role_name)
                    assign_role_to_user(user, role)
                except Role.DoesNotExist:
                    return render(request, 'create_user_with_roles.html', {'roles': Role.objects.all(), 'error_message': f'Role "{role_name}" does not exist'})
            
            return redirect('create_user_with_roles')
        except IntegrityError:
            return render(request, 'create_user_with_roles.html', {'roles': Role.objects.all(), 'error_message': 'An error occurred while creating the user'})
    
    roles = Role.objects.all()
    return render(request, 'create_user_with_roles.html', {'roles': roles})

def view_users_with_roles(request):
    users_with_roles = []
    users = User.objects.all()
    for user in users:
        roles = UserRole.objects.filter(user=user).values_list('role__name', flat=True)
        users_with_roles.append({'user': user, 'roles': roles})
    return render(request, 'view_users_with_roles.html', {'users_with_roles': users_with_roles})

def get_roles_for_user(user):
    user_roles = UserRole.objects.filter(user=user)
    roles = [user_role.role for user_role in user_roles]
    return roles

def delete_user_role(request, username):
    if request.method == 'POST':
        role_name = request.POST.get('role')
        try:
            user = User.objects.get(username=username)
            role = Role.objects.get(name=role_name)
            remove_user_role(user, role)
        except (User.DoesNotExist, Role.DoesNotExist):
            pass  # Handle the case where user or role does not exist
    return redirect('view_users_with_roles')
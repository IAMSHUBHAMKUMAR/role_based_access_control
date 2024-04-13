from .models import UserRole

def assign_role_to_user(user, role):
    UserRole.objects.create(user=user, role=role)

def remove_user_role(user, role):
    UserRole.objects.filter(user=user, role=role).delete()


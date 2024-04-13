from django.urls import path
from . import views

urlpatterns = [
    path('assign_role/', views.assign_role, name='assign_role'),
     path('create_user_with_roles/', views.create_user_with_roles, name='create_user_with_roles'),
     path('view_users_with_roles/', views.view_users_with_roles, name='view_users_with_roles'),
      path('auth/delete_user_role/<str:username>/', views.delete_user_role, name='delete_user_role'),

]

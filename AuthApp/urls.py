from django.urls import path
from . import views

urlpatterns = [
    # Frontend URLs
    path('', views.index, name='homepage'), 
    path('register/', views.register_page, name='register'), 
    path('register/verify/', views.verify_registration_page, name='verify_registration'),  
    path('login/', views.login_page, name='login'),  
    path('dashboard/', views.user_dashboard, name='dashboard'),  

    # for API's 
    path('api/csrf/', views.get_token, name='csrf_token'),
    path('api/register/', views.register, name='register_api'), 
    path('api/register/verify/', views.verify_registration, name='verify_registration_api'),
    path('api/login/', views.login_user, name='login_api'),  
    path('api/me/', views.get_user_details, name='user_details'),  
    path('api/logout/', views.logout_user, name='logout_api'),  
    path('api/users/',views.get_all_users),
]

import random
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CustomUser
from .serializers import LoginSerializer, UserSerializer
from django.middleware.csrf import get_token as django_get_token
from django.http import JsonResponse

from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def register_page(request):
    return render(request, 'register.html')

def verify_registration_page(request):
    return render(request, 'verify_registration.html')

def login_page(request):
    return render(request, 'login.html')

def user_dashboard(request):
    return render(request, 'user.html')


@api_view(["GET"])
def get_all_users(request):
    users = CustomUser.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def get_token(request):
    response = JsonResponse({"message": "CSRF cookie set"})
    response.set_cookie("csrftoken", django_get_token(request), httponly=True, samesite="Lax")
    return response

@api_view(["POST"])
def register(request):
    email = request.data.get("email")
    password = request.data.get("password")

    if CustomUser.objects.filter(email=email).exists():
        return Response({"error": "Email already registered"}, status=400)

    otp = str(random.randint(100000, 999999))
    user = CustomUser.objects.create_user(email=email, password=password, otp=otp)
    
    send_mail("OTP Verification", f"Your OTP is {otp}", "admin@example.com", [email])
    
    return Response({"message": "OTP sent to email"}, status=201)

@api_view(["POST"])
def verify_registration(request):
    email = request.data.get("email")
    otp = request.data.get("otp")

    try:
        user = CustomUser.objects.get(email=email, otp=otp)
        user.otp = None
        user.save()
        return Response({"message": "Registration verified"}, status=200)
    except CustomUser.DoesNotExist:
        return Response({"error": "Invalid OTP"}, status=400)

@api_view(["POST"])
def login_user(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    email = serializer.validated_data["email"]
    password = serializer.validated_data["password"]

    user = authenticate(email=email, password=password)
    if user:
        response = Response({"message": "Login successful"}, status=200)
        response.set_cookie("auth_token", user.id, httponly=True, samesite="Lax")
        return response
    return Response({"error": "Invalid credentials"}, status=400)

@api_view(["GET"])
def get_user_details(request):
    if not request.user.is_authenticated:
        return Response({"error": "Unauthorized"}, status=401)
    return Response(UserSerializer(request.user).data)

@api_view(["POST"])
def logout_user(request):
    response = Response({"message": "Logged out"}, status=200)
    response.delete_cookie("auth_token")
    return response

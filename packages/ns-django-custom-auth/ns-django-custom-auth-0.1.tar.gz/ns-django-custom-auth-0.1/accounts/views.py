from .models import *
from .constants import *
from .serializers import *
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status,permissions
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password


"""
SignUp Api
"""
class SignupApiView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        if not request.data.get("first_name"):
            return Response({"message":"Please enter first name","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
        if not request.data.get("last_name"):
            return Response({"message":"Please enter last name","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
        if not request.data.get("mobile_no"):
            return Response({"message":"Please enter mobile number","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
        if not request.data.get("email"):
            return Response({"message":"Please enter email","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
        if not request.data.get("password"):
            return Response({"message":"Please enter password","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create(
            first_name = request.data.get("first_name"),
            last_name = request.data.get("last_name"),
            email = request.data.get("email"),
            mobile_no = request.data.get("mobile_no"),
            password = make_password(request.data.get("password")),
            role_id = request.data.get("role_id"),
            gender = request.data.get("gender"),
        )
          
        try:
            device = Device.objects.get(user = user)
        except Device.DoesNotExist:
            device = Device.objects.create(user = user)
        if request.data.get('device_type'):
            device.device_type = request.data.get('device_type')
        if request.data.get('device_name'):
            device.device_name = request.data.get('device_name')
        if request.data.get('device_token'):
            device.device_token = request.data.get('device_token')
        
        device.save()
        data = UserSerializer(user,context = {"request":request}).data
        return Response({"message":"User Registered Successfully","data":data},status=status.HTTP_200_OK)


"""
Login Api
"""
class LoginApiView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        if not request.data.get("email"):
            return Response({"message":"Please enter email","status":status.HTTP_400_BAD_REQUEST})
        if not request.data.get("password"):
            return Response({"message":"Please enter password"},status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=request.data.get("email"), password=request.data.get("password"))

        if not user:
            return Response({"message":"Invalid Login Credentials.", "status":status.HTTP_400_BAD_REQUEST})
        if not user.is_active:
            return Response({"message":"Your account has been deactivated. Please contact admin to activate your account.","status":status.HTTP_400_BAD_REQUEST})

        login(request, user)
        try:
            token = Token.objects.get(user = user)
        except:
            token = Token.objects.create(user = user)

        try:
            device = Device.objects.get(user = user)
        except Device.DoesNotExist:
            device = Device.objects.create(user = user)

        if request.data.get('device_type'):
            device.device_type = request.data.get('device_type')
        if request.data.get('device_name'):
            device.device_name = request.data.get('device_name')
        if request.data.get('device_token'):
            device.device_token = request.data.get('device_token')
        
        device.save()

        data = UserSerializer(user,context = {"request":request}).data
        data.update({"token":token.key})   
        return Response({"message":"Logged In Successfully","data":data,"status":status.HTTP_200_OK}, status=status.HTTP_200_OK)

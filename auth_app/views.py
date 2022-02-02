from django.http.response import HttpResponse, JsonResponse
from django.views.generic.base import RedirectView
import requests
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import json
from .serializer import StudentSerializer,RegisterSerializer
from .models import Student,User
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from django.shortcuts import reverse
from django.shortcuts import render, redirect, HttpResponseRedirect

class Register(APIView):
    RegisterSerializer_Class=RegisterSerializer
    def get(self,request):
        return render(request, 'register.html')
    def post(self,request,format=None):
        serializer=self.RegisterSerializer_Class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            msg={
                'msg':"Registered Successfully"
            }
            return render(request, 'login.html',msg)
        else:
            return Response({"Message":serializer.errors,"status":status.HTTP_400_BAD_REQUEST})

class Login(APIView):
    def get(self,request):
        if 'logged_in' in request.COOKIES and 'Access_Token' in request.COOKIES:
            context = {
                'Access_Token': request.COOKIES['Access_Token'],
                'logged_in': request.COOKIES.get('logged_in'),
            }
            return render(request, 'studentBeautify.html', context)
        else:
            return render(request, 'login.html')

    def post(self,request,format=None):
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email,password)
        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')


        refresh = RefreshToken.for_user(user)
        response=render(request,'studentBeautify.html')
        response.set_cookie('Access_Token',str(refresh.access_token))
        response.set_cookie('logged_in', True)
        return response

def verification(header):
    return 'Authorization' not in header or not verifyToken(header['Authorization'])


class StudentAPI(APIView):

    authentication_classes=[JWTAuthentication]
    StudentSerializer_Class=StudentSerializer

    def get(self,request,format=None):
        print("I'm unauthenticated!")
        if verification(request.headers):
            return redirect('logout')
        DataObj=Student.objects.all()
        serializer=self.StudentSerializer_Class(DataObj,many=True)
        serializerData=serializer.data
        return Response(
    {
        "message": "Data Fetched",
        "code": "200",
        "status": True,
        "user": serializerData
    }
)
    # authentication_classes=[JWTAuthentication]
    def post(self,request,format=None):
        if verification(request.headers):
            return Response({"message": "Not Valid Token","code": "401","status": False})
        serializer=self.StudentSerializer_Class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            serializerData=serializer.data
            return Response({"status":status.HTTP_200_OK,"User":serializerData})
        else:
            return Response({"Message":serializer.errors,"status":status.HTTP_400_BAD_REQUEST})

class Logout(APIView):
    def get(self,request):
        try:
            response = HttpResponseRedirect(reverse('login'))
            # deleting cookies
            response.delete_cookie('Access_Token')
            response.delete_cookie('logged_in')
            return response
        except:
            return Response({"status":status.HTTP_400_BAD_REQUEST})
    def post(self,request):
        try:
            response = HttpResponseRedirect(reverse('login'))
            # deleting cookies
            response.delete_cookie('Access_Token')
            response.delete_cookie('logged_in')

            return response
        except:
            return Response({"status":status.HTTP_400_BAD_REQUEST})


def verifyToken(token):
    Data=requests.post('http://127.0.0.1:8000/verify',data={'token':str(token)})
    data=json.loads(Data.text)
    try:
        if(data['code']=="token_not_valid"):
            return False
        else:
            return True
    except:
        return True
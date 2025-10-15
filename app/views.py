from django.shortcuts import render
from django.shortcuts import redirect
from django.template.context_processors import request
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics, serializers, status
from .serializers import RegisterUserSerializer ,LoginSerializer,JobDetailSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from django.contrib.auth.decorators import permission_required
from django.test import RequestFactory
from django.contrib.auth.models import User
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken 
from .utils import api_response
# from nirmal_pms.app.models import JobDetail
# from nirmal_pms.app.serializers import JobDetailSerializer
# Create your views here.

def index(request):
    return HttpResponse("Yuvraj Soni")



class RegisterView(generics.CreateAPIView):

    queryset = Registration.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterUserSerializer
    
    
    def get(self,request):
        if request.method == 'GET':
            register =  Registration.objects.all()
            serializer =  RegisterUserSerializer(register,many=True)
            return Response(serializer.data)
        
        
class RegisterListView(APIView):
    serializer_class = RegisterUserSerializer
    permission_classes = [IsAuthenticated]
    def get(self,request):
        if request.method == 'GET':
            user_list = Registration.objects.all()
            serializer = RegisterUserSerializer(user_list, many=True)
            return Response(serializer.data)
        

class Loginview(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard-page') 
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        

class DashboardView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        user = request.user 
        register = Registration.objects.all()
        user_details = RegisterUserSerializer(register, many=True)
        job_data = JobDetail.objects.all()
        job_data = JobDetailSerializer(job_data,many=True)
        refresh = RefreshToken.for_user(user)
        
        user_info ={
            'username':user.username,
            'first_name':user.first_name
            
        }
        return api_response(
            data={
                "user_details": user_details.data,
                "job_data": job_data.data,
                "user_info":user_info
            },
            message=f"Welcome Dashboard {user.username}",
            status_code=status.HTTP_200_OK)
        
        
        
        # return Response({
        # 'messages':'Welcome to Dashboard',
        #   'user': {
        #         'username': user.username,
        #         'email': user.email,
        #         'first_name': user.first_name,
        #         'last_name': user.last_name,
        #         'refresh': str(refresh),
        #         'access':str(refresh.access_token)
        #     },
            
        #     'user_details':user_details.data,
        #     'job_serializers':job_data.data,
            
            
        # },status=status.HTTP_202_ACCEPTED)
    



class JobDetailView(APIView):
    
    def post(self,request):
        if request.method == 'POST':
            print("POST")
            
             
  
   
    
        
            
        
        
    

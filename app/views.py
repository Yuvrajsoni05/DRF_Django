from django.shortcuts import render
from django.shortcuts import redirect
from django.template.context_processors import request
from django.http import HttpResponse, HttpResponseRedirect
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
from django.views.decorators.csrf import csrf_exempt
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken 
from .utils import api_response
from .utils import CustomIsAuthenticated
from .decorators import custom_login_required


# from nirmal_pms.app.models import JobDetail
# from nirmal_pms.app.serializers import JobDetailSerializer
# Create your views here.
from django.utils.decorators import method_decorator

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
        

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    
   
   
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            login(request, user)
            return HttpResponseRedirect('dashboard')
            # return Response({
            #     'refresh': str(refresh),
            #     'access': str(refresh.access_token),
            #     'username': user.username,
            # })
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


        
# @method_decorator(custom_login_required,name='dispatch')
class DashboardView(APIView):
    permission_classes = (IsAuthenticated,)
    print(permission_classes)
    def get(self,request):
        user = request.user 
        register = Registration.objects.all()
        user_details = RegisterUserSerializer(register, many=True)
        job_data = JobDetail.objects.all()
        job_data = JobDetailSerializer(job_data,many=True)
        refresh = RefreshToken.for_user(user)
        
        user_info ={
            'username':user.username,
            'first_name':user.first_name,
            'refresh': str(refresh),
            'access':str(refresh.access_token),
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
    


@method_decorator(custom_login_required,name='dispatch')
class JobDetailView(APIView):
    permission_classes = (CustomIsAuthenticated,)
    def post(self,request):
        if request.method == 'POST':
            job_name = request.data.get("job_name")
            new_job = request.data.get("new_job_name")
            date = request.data.get("job_date")
            company_name = request.data.get("company_name")
            new_company = request.data.get("new_company")
            
            if not company_name and not new_company:
                return api_response(
                    message="Please provide company Name",
                    status_code=status.HTTP_400_BAD_REQUEST
                )
            if JobDetail.objects.filter(job_date=date,job_name=job_name).exists():    
                return api_response(
                    message="job already exists on this date. Kindly update the job.",
                    status_code=status.HTTP_400_BAD_REQUEST
                )
                
            serializers = JobDetailSerializer(data=request.data)
         
            try:
                if serializers.is_valid():
                    job_instance = serializers.save()
                    return api_response(message='New job added', status_code=status.HTTP_201_CREATED)
                else:
                    return api_response(message=f"Serializer errors: {serializers.errors}", status_code=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return api_response(message=f"An error occurred: {str(e)}", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

            


  
   
class JobUpdateDelete(APIView):
    def get(self,request,pk):
        try:
        
            job = JobDetail.objects.get(pk=pk)
        except JobDetail.DoesNotExist:
            return api_response(
                message="job dose not Exist",
                status_code=status.HTTP_404_NOT_FOUND
            )
        serializer = JobDetailSerializer(job)
        return api_response(data=serializer.data,message="Job data",status_code=status.HTTP_200_OK)

    
    def delete(self,request,pk):
        if request.method == 'DELETE':
            job = JobDetail.objects.get(pk=pk)
            job.delete()
            return api_response(
                message="Job Delete Successfully",
                status_code=status.HTTP_200_OK
            )
            
    

        
            
        
        
    

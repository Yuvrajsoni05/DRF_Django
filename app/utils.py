from rest_framework.response import Response
from django.contrib import messages
from rest_framework.permissions import IsAuthenticated
from rest_framework import status



def api_response(data=None,message=None ,status_code=None):
    response_data = {
        "message":message,
        "data" : data
    }

    return Response(response_data,status_code)








class CustomIsAuthenticated(IsAuthenticated):
    message = 'You must be logged in to access this resource.'
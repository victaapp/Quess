from django.http import HttpResponse
from urllib import request
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import *
# Create your views here.




class RegisterView(APIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    def post(self, request, *args, **kwargs):
        request_data = request.data.copy()
        request_data['username'] = request.data.get('email')
        serializer = self.serializer_class(data= request_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)




class QuestionApiView(APIView):
    serializer_class = QuesSerializer

    def get(self, request):
        qs = Question.objects.all().order_by('-id')
        if qs:
            serializer = self.serializer_class(qs, many=True)
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:    
            return Response({"result":"data not found"}, status = status.HTTP_404_NOT_FOUND)


class QuestionView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = QuestionSerializer
    http_method_names = ['post']
    
    # def get_queryset(self):
    #     query = Question.objects.all().order_by('-id')
    #     return query



    # def create(self, request, *args, **kwargs):
    #     user = request.user
    #     request_data = request.data.copy()
    #     request_data["ask_by"] = request.user.id
    #     serializer = self.serializer_class(data=request_data) # or request.data
    #                                     #    context={'author': user})
    #     if serializer.is_valid():
    #         import pdb;pdb.set_trace()
    #         serializer.save()
    #         return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        request_data = request.data.copy()
        request_data["ask_by"] = request.user.id
        serializer = self.serializer_class(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        


class que(APIView):
    def get(self,request):
        return HttpResponse("ASDAFD")
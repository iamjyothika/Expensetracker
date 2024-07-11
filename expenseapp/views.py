from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ExpenseModel,CategoryModel
from .serializers import *
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import login
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
# from django.db.models import Q




# {
#   "username":"Anagha",
#   "password":"anagha2000",
#   "email":"anagha28@gmail.com"
# }
#  "username":"Aleena",
#   "password":"aleena2001",
#   "email":"aleena20@gmail.com"
#  "username":"Nanthini",
#   "password":"nandhu1999",
#   "email":"nandhu26@gmail.com"

# Create your views here.
class UserRegistrationView(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        serializer=RegistrationSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        username=request.data.get("username")
        password = request.data.get("password")
        print(username,password)
        if not username or not password:
            return Response({"error": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_active:
                login(request, user)
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Account is disabled."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Invalid email or password."}, status=status.HTTP_400_BAD_REQUEST)
        
class ExpenseCreateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get(self,request):
        expense=ExpenseModel.objects.filter(user=request.user)
        serializer=ExpenseSerializer(expense,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
       

    
    def post(self, request):
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ExpenseDetailView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def patch(self,request,id):
        expense=get_object_or_404(ExpenseModel,id=id,user=request.user)
        serializer=ExpenseSerializer(expense,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,id):
        expense=get_object_or_404(ExpenseModel,id=id)
        expense.delete()
        return Response({"message":"Expense deleted"},status=status.HTTP_204_NO_CONTENT)
    
class CategoryCreateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get(self,request):
        category=CategoryModel.objects.filter(user=request.user)
        serializer=CategorySerializer(category,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def post(self,request):
        serializer=CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class CategoryDetailView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def patch(self,request,id):
        category=get_object_or_404(CategoryModel,id=id,user=request.user)
        serializer=CategorySerializer(category,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,id):
        category=get_object_or_404(CategoryModel,id=id)
        category.delete()
        return Response({"message":"category deleted"},status=status.HTTP_204_NO_CONTENT)
    


class CategoryList(APIView):
    permission_classes=[AllowAny]
    def get(self,request,format=None):
        category=CategoryModel.objects.all()
        serializer=CategorySerializer(category,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
 
    
class ExpenseFilterView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    
    def get(self, request):
        queryset = ExpenseModel.objects.all()

       
        date = request.query_params.get('date', None)
        category = request.query_params.get('category', None)
        amount = request.query_params.get('amount', None)


        if date:
            queryset = queryset.filter(date=date)
        if category:
            queryset = queryset.filter(category=category)
        if amount:
            queryset = queryset.filter(amount=amount)
        

        serializer = ExpenseSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


    

    



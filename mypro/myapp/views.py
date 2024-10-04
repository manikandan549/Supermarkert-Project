from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer,PurchaseSerializer,ProductSerializer,UserdetailsSerializer,StoreuserSerializer,StoreuserdetailsSerializer
from .models import User,Purchase,Product
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework import generics,viewsets
from rest_framework.exceptions import AuthenticationFailed
from django.http import JsonResponse
from django.db.models import Sum
from django.views.decorators.http import require_GET
from datetime import datetime as dt, timedelta
from django.core.exceptions import ObjectDoesNotExist 
import jwt,datetime

# Create your views here.
class RegisterView(APIView):
    def post(self,request):
        Serializer= UserSerializer(data=request.data)
        Serializer.is_valid(raise_exception=True)
        Serializer.save()
        return Response(Serializer.data)
    

class StoreuserregisterView(APIView):
    def post(self,request):
        Serializer= StoreuserSerializer(data=request.data)
        Serializer.is_valid(raise_exception=True)
        Serializer.save()
        return Response(Serializer.data)


class loginView(APIView):
    def post(self,request):
        email = request.data.get('email')
        password = request.data.get('password')

        user= User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found')
        
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')
        
        payload={'User_id':user.User_id,'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60),'iat': datetime.datetime.utcnow()}

        token=jwt.encode(payload,'secret',algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token,httponly=True)
        response.data = {'jwt': token}

        return response
    
class StoreuserloginView(APIView):
    def post(self,request):
        email = request.data.get('email')
        password = request.data.get('password')

        user= User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found')
        
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')
        
        if user.designation != 'Manager':
            raise AuthenticationFailed('unauthenticated User')
        
        payload={'User_id':user.User_id,'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60),'iat': datetime.datetime.utcnow()}

        token=jwt.encode(payload,'secret',algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt2', value=token,httponly=True)
        response.data = {'jwt2': token}

        return response
    

class UserView(APIView):
    def get(self,request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('unauthenticated')
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('unauthenticated')
        
        user=User.objects.filter(User_id=payload['User_id']).first()
        Serializer = UserdetailsSerializer(user)
        return Response(Serializer.data)


class StoreuserView(APIView):
    def get(self,request):
        token = request.COOKIES.get('jwt2')

        if not token:
            raise AuthenticationFailed('unauthenticated')
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('unauthenticated')
        
        user=User.objects.filter(User_id=payload['User_id']).first()
        Serializer = StoreuserdetailsSerializer(user)
        return Response(Serializer.data)


class logoutView(APIView):
    def post(self,request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {'message':'User Logout Successfuly done'}
        return response

class StoreuserlogoutView(APIView):
    def post(self,request):
        response = Response()
        response.delete_cookie('jwt2')
        response.data = {'message':'Storeuser Logout Successfuly done'}
        return response
        

class ProductViewset(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


@api_view(['POST'])
def make_purchase_stock(request):
    product_name = request.data.get('product_name')
    quantity_sold = request.data.get('quantity')

    # Check if product_name and quantity_sold are provided
    if not product_name or not quantity_sold:
        return Response('Both product_name and quantity_sold are required.', status=status.HTTP_400_BAD_REQUEST)

    try:
        product = Product.objects.get(product_name=product_name)
    except Product.DoesNotExist:
        return Response(f'Product "{product_name}" not found', status=status.HTTP_404_NOT_FOUND)

    # Check if product.stock is None (this indicates an error scenario)
    if product.stock is None:
        return Response(f'Stock information for "{product_name}" is unavailable. Contact support.', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    current_stock = product.stock

    if current_stock >= quantity_sold:
        product.stock -= quantity_sold
        product.save()
        serializer =PurchaseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response('Purchase successful. Stock updated.',status=status.HTTP_200_OK)
    else:
        return Response('Not enough stock available.', status=status.HTTP_400_BAD_REQUEST)
    

class PurchaseView(APIView):
    def post(self,request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('unauthenticated')
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('unauthenticated')
        
        product_name = request.data.get('product_name')
        quantity_sold = request.data.get('quantity')

        # Check if product_name and quantity_sold are provided
        if not product_name or not quantity_sold:
            return Response('Both product_name and quantity_sold are required.', status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(product_name=product_name)
        except Product.DoesNotExist:
            return Response(f'Product "{product_name}" not found', status=status.HTTP_404_NOT_FOUND)

        # Check if product.stock is None (this indicates an error scenario)
        if product.stock is None:
            return Response(f'Stock information for "{product_name}" is unavailable. Contact support.', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        current_stock = product.stock

        if current_stock >= quantity_sold:
            product.stock -= quantity_sold
            product.save()
            serializer = PurchaseSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
            return Response('Purchase successful. Stock updated.',status=status.HTTP_200_OK)
        else:
            return Response('Not enough stock available.', status=status.HTTP_400_BAD_REQUEST)



class total_shampoo_sales_last_7_daysView(APIView):
    def get(self,request):
        token = request.COOKIES.get('jwt2')

        if not token:
            raise AuthenticationFailed('unauthenticated')
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('unauthenticated')
        
        seven_days_ago = dt.now().date() - timedelta(days=7)
    
        try:
            total_shampoo_sales = Purchase.objects.filter(
                product_name='shampoo',
                date_of_purchase__gte=seven_days_ago
            ).aggregate(total_sales=Sum('amount'))['total_sales']
            
            if total_shampoo_sales is None:
                total_shampoo_sales = 0.0
            
            return JsonResponse({'total_shampoo_sales_last_7_days': total_shampoo_sales})
        
        except ObjectDoesNotExist:
            return JsonResponse({'total_shampoo_sales_last_7_days': 0.0})


class get_high_value_purchasesView(APIView):
    def get(self,request):
        token = request.COOKIES.get('jwt2')

        if not token:
            raise AuthenticationFailed('unauthenticated')
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('unauthenticated')
        
        purchases = Purchase.objects.values('User_id', 'date_of_purchase').annotate(total_amount=Sum('amount')).filter(total_amount__gt=1000)
    
        results = [{'User_id': purchase['User_id'], 'total_amount': purchase['total_amount']} for purchase in purchases]
        
        return JsonResponse({'high_value_purchases': results})


class get_total_items_purchasedView(APIView):

    def get(self,request,start_date,end_date):
        token = request.COOKIES.get('jwt2')

        if not token:
            raise AuthenticationFailed('unauthenticated')
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('unauthenticated')
        
        if not start_date or not end_date:
            return JsonResponse({'error': 'Both start_date and end_date are required as path parameters.'}, status=400)
    
        try:
            start_date = dt.strptime(start_date, '%Y-%m-%d').date()
            end_date = dt.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=400)
        
        total_items = Purchase.objects.filter(date_of_purchase__range=[start_date, end_date]).count()
        
        return JsonResponse({'total_items_purchased': total_items})


class ProductUpdateView(generics.UpdateAPIView):# this code working
    def get(self,request):
        token = request.COOKIES.get('jwt2')

        if not token:
            raise AuthenticationFailed('unauthenticated')
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('unauthenticated')
        queryset = Product.objects.all()
        serializer_class = ProductSerializer
        lookup_field = 'product_id' 

class ProductdeleteView(generics.DestroyAPIView):# this code working
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'product_id' 

class UserUpdateView(generics.UpdateAPIView):# this code working
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id' 

class UserdeleteView(generics.DestroyAPIView):# this code working
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id' 

class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer

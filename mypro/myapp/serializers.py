from rest_framework import serializers
from .models import User,Product,Purchase

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},  # Password should not be included in responses
        }

    def create(self, validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class StoreuserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'password','designation']
        extra_kwargs = {
            'password': {'write_only': True},  # Password should not be included in responses
        }

    def create(self, validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class UserdetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['User_id','name', 'email']

class StoreuserdetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['User_id','name', 'email','designation']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

# class PurchaseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Purchase
#         fields = '__all__'


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ['User_id','product_name', 'quantity','date_of_purchase']

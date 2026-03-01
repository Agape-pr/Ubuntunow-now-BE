from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Store

User = get_user_model()

class StoreSerializer(serializers.ModelSerializer):
    store_logo = serializers.ImageField(
        required=False,
        allow_null=True
    )
    store_description = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True
    )
    
    class Meta:
        model = Store
        fields = ['store_name', 'slug', 'store_description', 'store_logo']
    
    def to_internal_value(self, data):
        # Normalize empty strings to None for optional fields
        if 'store_description' in data and data['store_description'] == '':
            data['store_description'] = None
        return super().to_internal_value(data)

class UserRegistrationSerializer(serializers.ModelSerializer):
    account_type = serializers.ChoiceField(
        choices=[('buyer', 'Buyer'), ('seller', 'Seller')],
        write_only=True
    )
    password = serializers.CharField(write_only=True)
    store = StoreSerializer(required=False, allow_null=True)


    def validate(self, attrs):
        account_type = attrs.get('account_type')
        store_data = attrs.get('store')

        # Seller must provide store data with store_name
        if account_type == 'seller':
            if not store_data:
                raise serializers.ValidationError({
                    "store": "Store data is required for sellers."
                })
            if not store_data.get('store_name') or not store_data.get('store_name', '').strip():
                raise serializers.ValidationError({
                    "store": {"store_name": "Store name is required for sellers."}
                })
            # Normalize empty string to None for optional fields
            if store_data.get('store_description') == '':
                store_data['store_description'] = None

        # Buyer must NOT provide store data
        if account_type == 'buyer' and store_data:
            raise serializers.ValidationError({
                "store": "Buyers are not allowed to create a store."
            })

        return attrs


    class Meta:
        model = User
        fields = ['email', 'password', 'account_type', 'phone_number', 'store']

    def create(self, validated_data):
        store_data = validated_data.pop('store', None)
        password = validated_data.pop('password')
        account_type = validated_data.pop('account_type')

        role = (
            User.Role.SELLER
            if account_type == 'seller'
            else User.Role.BUYER
        )

        user = User.objects.create_user(
            email=validated_data['email'],
            password=password,
            phone_number=validated_data.get('phone_number'),
            role=role,
            username=validated_data['email'],
            is_active=False,
        )

        if role == User.Role.SELLER:
            Store.objects.create(user=user, **store_data)

        return user
class UserDetailSerializer(serializers.ModelSerializer):
    store = StoreSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'role', 'phone_number', 'store']

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Add user info to the response
        user_serializer = UserDetailSerializer(self.user)
        data['user'] = user_serializer.data
        
        return data

class PublicStoreSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    store_logo = serializers.ImageField(read_only=True)

    class Meta:
        model = Store
        fields = ['store_name', 'slug', 'store_description', 'store_logo', 'created_at', 'products']

    def get_products(self, obj):
        from apps.products.serializers import ProductSerializer
        # Only surface active products on the public store page
        active_products = obj.products.filter(is_active=True)
        return ProductSerializer(active_products, many=True).data

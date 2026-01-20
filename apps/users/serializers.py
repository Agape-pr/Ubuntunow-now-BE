from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Store

User = get_user_model()

class StoreSerializer(serializers.ModelSerializer):
    store_logo = serializers.ImageField(
        required=False,
        allow_null=True
    )
    class Meta:
        model = Store
        fields = ['store_name', 'store_description', 'store_logo']

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

        # Seller must provide store data
        if account_type == 'seller' and not store_data:
            raise serializers.ValidationError({
                "store": "Store data is required for sellers."
            })

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
        )

        if role == User.Role.SELLER:
            Store.objects.create(user=user, **store_data)

        return user
class UserDetailSerializer(serializers.ModelSerializer):
    store = StoreSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'role', 'phone_number', 'store']

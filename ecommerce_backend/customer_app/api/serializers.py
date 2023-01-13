from rest_framework import serializers
from django.contrib.auth.models import User

from customer_app.models import AdminUser, Customer

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password',}, write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
        
    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        
        if password != password2:
            raise serializers.ValidationError({'error': 'Password1 and Password2 are not same!'})
        
        input_email = self.validated_data['email']
        if User.objects.filter(email=input_email).exists():
            raise serializers.ValidationError({'error': 'Email already exists!'})
        
        account = User(username=self.validated_data['username'], email=input_email)
        account.set_password(password)
        account.save()
        
        return account


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminUser
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    class Meta:
        model = Customer
        fields = '__all__'
    
    def get_user(self, object):
        user_info = User.objects.filter(pk=object.user.id).first()
        serializer = UserSerializer(user_info)
        return serializer.data
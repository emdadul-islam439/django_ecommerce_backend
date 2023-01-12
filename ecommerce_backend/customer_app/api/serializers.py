from rest_framework import serializers
from django.contrib.auth.models import User

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
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class AdminUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default='', related_name='adminUser')
    
    def __str__(self) -> str:
        return self.user.username
    
    
class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    # username, email, password -> in the 'user' table
    user = models.OneToOneField(User, on_delete=models.CASCADE, default='', related_name='customer', null=True)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    image = models.ImageField(default='default.png', upload_to="profile_pics")
    
    def __str__(self) -> str:
        return str(self.user)
    

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class AdminUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default='', related_name='adminUser')
    
    def __str__(self) -> str:
        return self.user.username
    
    
class Customer(models.Model):
    # username, email, password -> in the 'user' table
    user = models.OneToOneField(User, on_delete=models.CASCADE, default='', related_name='customer', null=True, blank=True)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)
    image = models.ImageField(default='default.png', upload_to="profile_pics")
    
    def __str__(self) -> str:
        if self.user is None:
            return f"Customer ID = {self.pk} (customer.user is NONE)"
        else:
            return f"username = {str(self.user.username)} | email = {str(self.user.email)}"
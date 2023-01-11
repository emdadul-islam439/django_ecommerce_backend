from django.contrib import admin
from customer_app.models import AdminUser, Customer

# Register your models here.
class CustomerAdminModel(admin.ModelAdmin):
    search_fields = ("user__username",)
    
    
admin.site.register(AdminUser)
admin.site.register(Customer, CustomerAdminModel)

from crum import get_current_user

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class CompanyName(models.Model):
    company_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  
    
    def __str__(self):
        return self.company_name
  
class Item(models.Model):
    item_name = models.CharField(max_length=50, unique=True)
    item_price = models.IntegerField(default=0)
    company_name = models.ForeignKey(CompanyName, on_delete= models.CASCADE,default=None, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True) 
    
    def __str__(self):
        return self.item_name 
    
class Stock(models.Model):
    user_name = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    item_name = models.ForeignKey(Item, on_delete = models.CASCADE)
    item_qty = models.IntegerField(default=0)
    is_admin_updated = models.BooleanField(default=False, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = (('user_name', 'item_name'),)
    
    def __str__(self):
        return self.item_name.item_name
    
    def save(self, *args, **kwargs):
        print('User is ', get_current_user().is_superuser)
        if get_current_user().is_superuser:
            self.is_admin_updated = True
        else:
            self.is_admin_updated = False
        super(Stock, self).save(*args, **kwargs)
    
# Stock History
class StockHistory(models.Model):
    user_name = models.ForeignKey(User, on_delete=models.CASCADE, default=None, editable=False)
    item_name = models.ForeignKey(Item, on_delete = models.CASCADE, editable=False)
    item_qty = models.IntegerField(default=0, editable=False)
    is_admin_updated = models.BooleanField(default=False, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)  
    updated_at = models.DateTimeField(auto_now=True, editable=False)  
    
    
    def __str__(self):
        return self.item_name.item_name
    
class Sells(models.Model):
    user_name = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    item_name = models.ForeignKey(Item, on_delete = models.CASCADE)
    company_name = models.ForeignKey(CompanyName, on_delete= models.CASCADE, default="", blank=True, null=True)
    item_qty = models.IntegerField(default=1)
    price = models.IntegerField()
    comment = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return self.item_name.item_name
    

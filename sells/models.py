from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# class BaseModel(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True)  
#     updated_at = models.DateTimeField(auto_now=True)  
  
class Item(models.Model):
    item_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True) 
    
    def __str__(self):
        return self.item_name 
    
class Stock(models.Model):
    user_name = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    item_name = models.ForeignKey(Item, on_delete = models.CASCADE)
    item_qty = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  
    
    class Meta:
        unique_together = (('user_name', 'item_name'),)
    
    def __str__(self):
        return self.item_name.item_name
    
class Sells(models.Model):
    user_name = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    item_name = models.ForeignKey(Item, on_delete = models.CASCADE)
    item_qty = models.IntegerField(default=1)
    price = models.IntegerField()
    comment = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return self.item_name.item_name
    
# class Stock(models.Model):
#     user_name = models.ForeignKey(User, on_delete=models.CASCADE)
#     item_name = models.CharField(max_length=50)
#     item_qty = models.IntegerField()
#     created_date = models.DateTimeField(auto_now_add=True)
#     date = models.DateField(auto_now=True)
#     time = models.TimeField(auto_now=True)
    
#     class Meta:
#         unique_together = (("user_name", "item_name"),)
    
#     def __str__(self):
#         return self.item_name
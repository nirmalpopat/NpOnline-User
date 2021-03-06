from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Stock, StockHistory, Item, User

# i want to store records when i update stock

@receiver(post_save, sender=Stock)
def fun(sender, instance, created, **kwargs):    
    StockHistory(user_name=instance.user_name, item_name=instance.item_name, item_qty=instance.item_qty, is_admin_updated = instance.is_admin_updated).save()
    
@receiver(post_save, sender=Item)
def fun(sender, instance, created, **kwargs):
    for user in User.objects.all():
        Stock(user_name = user, item_name = instance).save()
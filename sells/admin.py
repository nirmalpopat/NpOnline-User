from django.contrib import admin
from .models import Stock, Sells, Item, CompanyName, StockHistory
# Register your models here.

class StockAdmin(admin.ModelAdmin):
    list_display = ('user_name','item_name', 'item_qty', 'is_admin_updated', 'created_at', 'updated_at')
    
class StockHistoryAdmin(admin.ModelAdmin):
    list_display = ('user_name','item_name', 'item_qty', 'is_admin_updated', 'created_at', 'updated_at')
    
class SellsAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'item_name', 'company_name', 'item_qty', 'price', 'comment', 'created_at', 'updated_at')
    
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'item_name', 'item_price', 'created_at', 'updated_at')

class CompanyNameAdmin(admin.ModelAdmin):
    list_display = (
        'company_name',
        'created_at',
        'updated_at',
        )

admin.site.register(Stock, StockAdmin)
admin.site.register(StockHistory, StockHistoryAdmin)
admin.site.register(Sells, SellsAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(CompanyName, CompanyNameAdmin)

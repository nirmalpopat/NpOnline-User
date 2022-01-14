from django.contrib import admin
from .models import Stock, Sells, Item
# Register your models here.

class StockAdmin(admin.ModelAdmin):
    list_display = ('user_name','item_name', 'item_qty','created_at', 'updated_at')
    #prepopulated_fields = {'slug': ('product_name',)}
    #list_display_links = ('email', 'first_name', 'last_name', 'username')
    #readonly_fields = ('last_login','date_joined')
    #ordering = ('-date_joined',)
    
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    
class SellsAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'item_name', 'item_qty', 'price', 'comment', 'created_at', 'updated_at')
    #prepopulated_fields = {'slug': ('product_name',)}
    #list_display_links = ('email', 'first_name', 'last_name', 'username')
    #readonly_fields = ('last_login','date_joined')
    #ordering = ('-date_joined',)
    
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    
class ItemAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'created_at', 'updated_at')
    
# admin.site.register(Stock, StocktAdmin)
# admin.site.register(Sells, SellsAdmin)

admin.site.register(Stock, StockAdmin)
admin.site.register(Sells, SellsAdmin)
admin.site.register(Item, ItemAdmin)

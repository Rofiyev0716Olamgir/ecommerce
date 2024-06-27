from django.contrib import admin
from .models import CartItem, Order, Promo


@admin.register(Promo)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'discount', 'min_price', 'expire_date', 'is_expired', 'created_date',)
    date_hierarchy = 'created_date'
    list_filter = ('is_expired',)
    filter_horizontal = ('members', )
    readonly_fields = ('created_date', )
    search_fields = ('user__username', 'user__full_name',)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'unit_price', 'quantity', 'amount', 'is_ordered', 'created_date')
    search_fields = ('product__title', 'product__username', 'user_ful_name')
    date_hierarchy = 'created_date'
    list_filter = ('is_ordered', )
    readonly_fields = ('created_date',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount', 'is_delivered', 'created_date',)
    date_hierarchy = 'created_date'
    list_filter = ('is_delivered',)
    readonly_fields = ( 'modified_date', 'created_date')
    search_fields = ('user__username', 'user__full_name', )



from django.contrib import admin
from .models import Product
from .models import Cart , OrderPlaced, Payment


class ProductAdmin(admin.ModelAdmin):
    list_display = ('gadgetName', 'category','gadgetImage' ,'price', 'is_available', 'created_at', 'updated_at')
    search_fields = ('gadgetName', 'category')
    list_filter = ('category', 'is_available')
    ordering = ('created_at',)

    fieldsets = (
        (None, {
            'fields': ('gadgetName', 'category', 'price', 'gadgetImage')
        }),
        ('Availability', {
            'fields': ('is_available',),
        }),
        ('Additional Information', {
            'fields': ('description',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),  # Include updated_at for display
            'classes': ('collapse',),
        }),
    )

    readonly_fields = ('created_at', 'updated_at')  # Mark both fields as readonly

admin.site.register(Product, ProductAdmin)



admin.site.site_header = 'Welcome'
admin.site.site_title = 'TechNestle'
admin.site.index_title = 'Welcome to the Admin Panel'

class CartAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'product', 'quantity']
  

admin.site.register(Cart, CartAdmin)

class OrderPlacedAdmin(admin.ModelAdmin):
    list_display = ('user', 'Address', 'product', 'quantity', 'ordered_date', 'status')  # Fields to display
    list_filter = ('status', 'ordered_date')  # Add filters for better navigation
    search_fields = ('user__username', 'product__name')  # Enable searching by username and product name
    ordering = ('-ordered_date',)  # Order by the ordered date, most recent first

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'razorpay_order_id', 'razorpay_payment_status', 'paid')
    search_fields = ('user__username', 'razorpay_order_id')
    list_filter = ('paid', 'razorpay_payment_status')

# Register the models with the admin site

admin.site.register(OrderPlaced, OrderPlacedAdmin)
admin.site.register(Payment, PaymentAdmin)
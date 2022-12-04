from django.contrib import admin
from django import forms
from mptt.admin import MPTTModelAdmin
from.models import *
from modeltranslation.admin import TranslationAdmin
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin

# Register your models here.
# admin.site.register(Category)
# admin.site.register(ProductType)
# admin.site.register(ProductSpecification)
# admin.site.register(Product)
# admin.site.register(ProductSpecificationValue)
admin.site.register(Profile)



@admin.register(Category)
class CategoryAdmin(TranslationAdmin):

    def image_tag(self, obj):
        return format_html('<img src="{}"height="75" />'.format(obj.image.url))
    image_tag.short_description = 'Image'

    list_display = ('name','is_active', 'image_tag')
    search_fields = ('name',)
    list_filter = ['is_active']

class ProductSpecificationInline(admin.TabularInline):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
          kwargs['queryset'] = ProductSpecification.objects.filter(product_id= Product.id)
    model = ProductSpecification

@admin.register(ProductType)
class ProductTypeAdmin(TranslationAdmin):
    inlines = [
        ProductSpecificationInline,
    ]
    search_fields = ('name', )

class ProductImageInline(admin.TabularInline):
    model = ProductImage

class ProductSpecificationValueInline(admin.TabularInline):
    model = ProductSpecificationValue

@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    inlines = [
        ProductSpecificationValueInline, ProductImageInline
    ]

    def image_tag(self, obj):
        return format_html('<img src="{}"height="75" />'.format(obj.image.url))
    image_tag.short_description = 'Image'

    list_display = ('title','category', 'regular_price', 'discount_price', 'is_active','image_tag')
    search_fields = ('title', 'desciption')
    list_filter = ['category','is_active']


@admin.register(orders)
class orders(admin.ModelAdmin):
    list_display = ('user','product', 'quantity', 'amount', 'Order_number','created_at', 'status')
    search_fields = ('Order_number', 'user','product')
    list_filter = ['status']


@admin.register(Contact)
class Contact(admin.ModelAdmin):
    list_display = ('email','name', 'subject')
    search_fields = ('email', 'name','subject')
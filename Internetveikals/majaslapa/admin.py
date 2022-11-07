from django.contrib import admin
from django import forms
from mptt.admin import MPTTModelAdmin
from.models import *
from modeltranslation.admin import TranslationAdmin

# Register your models here.
# admin.site.register(Category)
# admin.site.register(ProductType)
# admin.site.register(ProductSpecification)
# admin.site.register(Product)
# admin.site.register(ProductSpecificationValue)
admin.site.register(Profile)



@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    pass

class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification

@admin.register(ProductType)
class ProductTypeAdmin(TranslationAdmin):
    inlines = [
        ProductSpecificationInline,
    ]

class ProductImageInline(admin.TabularInline):
    model = ProductImage

class ProductSpecificationValueInline(admin.TabularInline):
    model = ProductSpecificationValue

@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    inlines = [
        ProductSpecificationValueInline, ProductImageInline
    ]

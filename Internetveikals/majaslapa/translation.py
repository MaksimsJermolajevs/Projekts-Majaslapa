from modeltranslation.translator import register, TranslationOptions, translator
from .models import Product, ProductType, Category

@register(Product)
class ProductTranslationOption(TranslationOptions):
    fields = ('title', 'desciption')


@register(Category)
class CategoryTranslationOption(TranslationOptions):
    fields = ('name',)

@register(ProductType)
class TypeTranslationOption(TranslationOptions):
    fields = ('name',)
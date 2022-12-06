from modeltranslation.translator import register, TranslationOptions, translator
from .models import Product, Category, Specification

@register(Product)
class ProductTranslationOption(TranslationOptions):
    fields = ('title', 'desciption')


@register(Category)
class CategoryTranslationOption(TranslationOptions):
    fields = ('name',)


@register(Specification)
class SpecificationTranslationOption(TranslationOptions):
    fields = ('specification',)


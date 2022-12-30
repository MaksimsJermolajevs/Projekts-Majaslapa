from modeltranslation.translator import register, TranslationOptions, translator
from .models import Product, Category, Specification, Specification_name

@register(Product)
class ProductTranslationOption(TranslationOptions):
    fields = ('title', 'desciption')


@register(Category)
class CategoryTranslationOption(TranslationOptions):
    fields = ('name',)


@register(Specification)
class SpecificationTranslationOption(TranslationOptions):
    fields = ('specification_value',)

@register(Specification_name)
class SpecificationTranslationOption(TranslationOptions):
    fields = ('specification',)

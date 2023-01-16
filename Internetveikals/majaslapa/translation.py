from modeltranslation.translator import register, TranslationOptions, translator
from .models import Product, Category, ProductSpecification, ProductSpecificationValue

@register(Product)
class ProductTranslationOption(TranslationOptions):
    fields = ('title', 'desciption')


@register(Category)
class CategoryTranslationOption(TranslationOptions):
    fields = ('name',)


@register(ProductSpecification)
class ProductSpecificationTranslationOption(TranslationOptions):
    fields = ('name',)

@register(ProductSpecificationValue)
class ProductSpecificationValueTranslationOption(TranslationOptions):
    fields = ('value',)

# @register(Specification)
# class SpecificationTranslationOption(TranslationOptions):
#     fields = ('specification_value',)

# @register(Specification_name)
# class SpecificationTranslationOption(TranslationOptions):
#     fields = ('specifications',)

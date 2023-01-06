
from django.conf import settings
from django.db.models import CharField, Model
from django.urls import reverse
from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from autoslug import AutoSlugField



class Category(MPTTModel):
    name = models.CharField(
    verbose_name = ('Nosaukums'),
    help_text=('Request and unique'),
    max_length = 255,
    unique= True
    )

    slug = AutoSlugField(populate_from='name',max_length=255, verbose_name = ('tīmekļa adreses identifikācija'), unique=True)
    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name = 'children',verbose_name = ('Līdzīgie produkti'))
    is_active = models.BooleanField(default=True,verbose_name = ('Ir aktīvs'))
    image =models.ImageField(
        verbose_name= 'Attēls priekš kategorijas',
        help_text='Augšupielādējiet produkta attēlu',
        upload_to='images_category/',
        default='images_category/no-image.png'
    )

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = ('Kategorija')
        verbose_name_plural = ('Kategorījas')

    def get_absolute_url(self):
        return reverse("search", kwargs={'post_slug':self.slug})

    def __str__(self):
        return self.name



class Product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.RESTRICT, verbose_name = ('Kategorija'))
    title = models.CharField(
        verbose_name = ('Nosaukums'),
        help_text=('nepieciešams'),
        max_length = 255
    )

    desciption = models.TextField(verbose_name='Apraksts', help_text=('nav nepieciešams'), blank=True)
    slug = AutoSlugField(populate_from='title',max_length=255, verbose_name = ('tīmekļa adreses identifikācija'))
    regular_price = models.DecimalField(
        verbose_name='Parastā cena',
        help_text = ('Maksimums 9999.99'),
        error_messages= {
            'name' : {
                'max_lenght': 'Cenai jābūt no 0 līdz 9999,99!'
            }
        },
        max_digits=6,
        decimal_places=2,
        )

    discount_price = models.DecimalField(
        verbose_name=('Atlaides cena'),
        help_text= ('Maksimalais ir 9999.99'),
        error_messages={
            'name' : {
                'max_lenght': 'Cenai jābūt no 0 līdz 9999,99!'
            }
        },
        max_digits=6,
        decimal_places=2,
        null= True,
        blank= True
    )

    quantity = models.IntegerField(default= 0)

    is_active = models.BooleanField(
        verbose_name = 'Produkta redzamība',
        help_text = 'Mainīt produkta redzamību',
        default=True
    )
    image =models.ImageField(
        verbose_name= 'Attēls',
        help_text='Augšupielādējiet produkta attēlu',
        upload_to='images-product/',
        default='images-product/no-image.png'
    )
    created_at = models.DateTimeField(('Izveidots plkst'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(('Atjaunināts plkst'), auto_now_add=True, editable=False)


    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Prece'
        verbose_name_plural = ('Preces')

    def get_absolute_url(self):
        return reverse("product", kwargs={'product_slug':self.slug})

    def __str__(self):
        return self.title

class Specification(models.Model):
    specification_value = models.CharField(max_length=255)
    def __str__(self):
        return self.specification_value

class Specification_name(models.Model):
    specifications = models.CharField(max_length=255 , null=True)
    # product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name=('Produkta_specifikacijaa'), null=True)
    # specification = models.ForeignKey(Specification, on_delete=models.CASCADE)
    def __str__(self):
        return self.specifications

class All_specification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name=('Produkta_specifikacijaa'), null=True)
    specification = models.ForeignKey(Specification, on_delete=models.CASCADE, related_name=('Specification_name'), null=True)
    Specification_name = models.ForeignKey(Specification_name, on_delete=models.CASCADE, related_name=('Specification_name'), null=True)

class ProductImage(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name=('Produkta_attēls'))
    image =models.ImageField(
        verbose_name= 'Attēls',
        help_text='Augšupielādējiet produkta attēlu',
        upload_to='images/',
        default='images/default.png'
    )

    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        verbose_name = 'Produkta attēls'
        verbose_name_plural = 'Produkta attēli'



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # Delete profile when user is deleted
    image = models.ImageField(default='default.png', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'


class orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    Order_number = models.IntegerField(validators=[
            MaxValueValidator(9999999999),
            MinValueValidator(1)
        ])
    quantity = models.IntegerField()
    amount = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        )
    created_at = models.DateTimeField( auto_now_add=True, editable=False)
    Orderstatus = (
        ('Apstrāda', 'Apstrāda'),
        ('Sūta', 'Sūta'),
        ('Atcelts', 'Atcelts'),
        ('Pabeigts','Pabeigts'),
    )
    status = models.CharField(max_length=150, choices=Orderstatus, default='Apstrāda')


class Contact(models.Model):
    name = models.CharField(max_length=200, null=False)
    email = models.EmailField(null=False)
    subject = models.CharField(max_length=200, null=False)
    details = models.TextField(null=False)
    def __str__(self):
        return self.name



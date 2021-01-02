from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from datetime import date
from django.utils.timezone import now
from accounts.models import User
# Create your models here.
UNIT = (

    ('kilograms', 'KILOGRAMS'),
    ('litres', 'LITRES'),

)


class Product(models.Model):
    name = models.CharField(max_length=50)
    icon = models.ImageField(default='product.png', upload_to='product_images')

    def __str__(self):
        return str(self.name)


class Chalan(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(error_messages={
        'required': "Quantity must be provided"})

    unit = models.CharField(choices=UNIT, max_length=10,
                            blank=True, null=True, default="")
    imported_from = models.CharField(max_length=200)
    customs_clearance_no = models.PositiveBigIntegerField(unique=True, error_messages={
        'unique': "A user with that email already exists.",
    }, null=True, blank=True)
    # transaction_level = models.IntegerField(default=0, null=True)
    price = models.PositiveIntegerField()
    import_date = models.DateField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.product.name} - {self.owner.username}'


class SellProduct(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    buyer = models.CharField(max_length=30)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(error_messages={
        'required': "Quantity must be provided"})
    unit = models.CharField(choices=UNIT, max_length=20)
    price = models.PositiveIntegerField()
    pending = models.BooleanField(default=True, null=True)
    # transaction_level = models.IntegerField(default=0)
    sell_date = models.DateField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.seller.username} -sold- {self.product.name}'


# @receiver(post_save, sender=SellProduct)
# def create_object(sender, instance, created, **kwargs):
#     user = User.objects.get(trade_license_no=instance.buyer)
#     print(user)
#     if created and instance.pending == False:
#         Chalan.objects.create(owner=user, product=instance.product, quantity=instance.quantity,
#                               unit=instance.unit, price=instance.price, import_date=instance.sell_date, imported_from=instance.seller.username)
#         post_save.connect(create_object, sender=SellProduct)

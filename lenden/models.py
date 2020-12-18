from django.db import models
from datetime import date
from django.utils import timezone
from accounts.models import User
# Create your models here.
UNIT = (
    ('tons','TON'),
    ('metrictons', 'METRIC TONS'),
    ('kilograms', 'KILOGRAMS'),
    ('litres','LITRES'),
    ('gallons', 'GALLONS'),
    
)

class Product(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length = 200)
    quantity = models.PositiveBigIntegerField(error_messages={
        'required': "Quantity must be provided"})

    unit = models.CharField(choices = UNIT, max_length=10, blank=True, null=True, default="")
    imported_from = models.CharField(max_length = 200)
    customs_clearance_no = models.PositiveBigIntegerField(unique = True, error_messages={
                                  'unique': "A user with that email already exists.",
                              })
    import_date = models.DateField(default = timezone.now)


    def __str__(self):
        return f'{self.name} - {self.owner.username}'



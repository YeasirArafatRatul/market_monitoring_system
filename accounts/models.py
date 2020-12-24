from django.db import models
from accounts.managers import UserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from datetime import date
import random
# Create your models here.


# IF YOU THINK THERE SHOULD BE MORE DATA FIELD THEN ADD THEM OR LEAVE A COMMNET LIKE THIS


ROLE = (
    ('retailer', 'Retailer'),
    ('importer', 'Importer'),
    ('wholeseller', 'Whole Seller'),
)


def randint():
    return random.randint(1000, 9999)


class User(AbstractUser):
    username = models.CharField(unique=True, max_length=15, error_messages={
        'unique': "A user with that name already exists.",
    })
    email = models.EmailField(unique=True, blank=False,
                              error_messages={
                                  'unique': "A user with that email already exists.",
                              })
    trade_license_no = models.PositiveBigIntegerField(unique=True, null=True, blank=False,
                                                      error_messages={
                                                          'unique': "A user with that trade license is already exists.",
                                                      })
    role = models.CharField(choices=ROLE, max_length=15, error_messages={
        'required': "Role must be provided"
    })
    signed_up = models.DateField(default=date.today())

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username', ]

    # @property
    # def usercode(self):

    #     return str(self.username + str(randint())).upper()

    def __str__(self):
        return f"{self.role} - {self.trade_license_no}"

    objects = UserManager()


class UserProfileManager(models.Manager):

    def profile_update(self, image):
        profile_update_obj = self.model(image=image)


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    image = models.ImageField(blank=True, null=True,
                              default='avatar.png', upload_to='profile_pics')
    division = models.CharField(
        max_length=30, null=True, blank=True)
    district = models.CharField(
        max_length=30, null=True, blank=True)
    upazila = models.CharField(
        max_length=30, null=True, blank=True)

    industry_type = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.user.email}'

    objects = UserProfileManager()


# signal.py
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        post_save.connect(create_profile, sender=User)

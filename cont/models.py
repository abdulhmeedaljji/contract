from django.db import models

# Create your models here.

from datetime import date

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.contrib.auth.models import Group as AuthGroup
from django.contrib.auth.models import Permission as AuthPermission

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)


    # custom fields for different user types
    is_supplier = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.full_name or self.email
    
    def get_short_name(self):
        return self.email
    
    
    
    


class Ordeer(models.Model):
    nupco_po = models.CharField(max_length=125)
    customer_po=models.CharField(max_length=250)
    locations = models.CharField(max_length=250)
    issue_delivery = models.DateField()

    
    PO_item_number = models.CharField(max_length=125)
    nupco_Gen_code = models.CharField(max_length=125)
    nupco_Trade_code = models.CharField(max_length=125)
    desscription = models.CharField(max_length=125)
    Ordeer_Qty = models.CharField(max_length=125)
    available_Qty = models.IntegerField(blank=True, null=True,default=0)
    Requested_Qty = models.IntegerField(blank=True, null=True,default=0)

    date_delivery = models.DateField(blank=True, null=True, default=date.today)
    creation_delivery = models.DateField(blank=True, null=True, default=date.today)
    
    status = models.CharField(max_length=250,blank=True, null=True,default="")
    
    def __str__(self):
       return  self.nupco_po
    
   
    
    
    
    
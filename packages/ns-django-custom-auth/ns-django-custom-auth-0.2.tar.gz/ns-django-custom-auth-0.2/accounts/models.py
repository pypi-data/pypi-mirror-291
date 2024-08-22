from .constants import *
from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class User(AbstractBaseUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    mobile_code = models.CharField(max_length=30,blank=True,null=True)
    mobile_no = models.CharField(max_length=30,blank=True,null=True)
    age = models.IntegerField(blank=True,null=True)
    gender = models.PositiveIntegerField(choices=GENDER, null=True, blank=True)
    profile_pic = models.FileField(upload_to='profile_pic/', blank=True, null=True)
    role_id = models.PositiveIntegerField(default=ADMIN,choices=USER_ROLE,null=True, blank=True)
    social_id = models.CharField(max_length=255, null=True, blank=True)
    social_type = models.PositiveIntegerField(choices=SOCIAL_TYPE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True,null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    class Meta:
        managed = True
        db_table = 'tbl_user'

class Device(models.Model):
    user = models.ForeignKey('User',null=True,blank=True,on_delete=models.CASCADE)
    device_type = models.PositiveIntegerField(choices=DEVICE_TYPE,null=True,blank=True)
    device_name = models.CharField(max_length=255,null=True,blank=True)
    device_token = models.TextField(null=True,blank=True)
    ip_address = models.CharField(max_length=255,null=True,blank=True)
    device_model = models.CharField(max_length=255,null=True,blank=True)
    imei = models.CharField(max_length=255,null=True,blank=True)

    class Meta:
        managed = True
        db_table = 'tbl_device'

    def __str__(self):
        return str(self.device_name)
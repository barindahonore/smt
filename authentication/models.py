from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

from core.models import Isibo

# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    GENDER_CHOICES = (
        ('MALE', 'MALE'),
        ('FEMALE', 'FEMALE')
    )
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True)
    picture = models.ImageField(default='/default.jpg', blank=True, null=True, upload_to='users/profiles/')
    province = models.CharField(max_length=30, null=True, blank=True)
    district = models.CharField(max_length=30, null=True, blank=True)
    sector = models.CharField(max_length=30, null=True, blank=True)
    cell = models.CharField(max_length=30, null=True, blank=True)
    village = models.CharField(max_length=30, null=True, blank=True)
    isibo = models.ForeignKey(Isibo, null=True, blank=True, on_delete=models.CASCADE)
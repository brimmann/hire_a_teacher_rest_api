from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.authtoken.models import Token


class UserManager(BaseUserManager):
    """ User Manager that knows how to create users via email instead of username """

    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    objects = UserManager()
    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"
    username = None
    first_name = None
    last_name = None
    email = models.EmailField("email address", blank=False, null=False, unique=True)
    type = models.CharField(max_length=30)

    # teacher_detail = models.ForeignKey(TeacherDetail, on_delete=models.CASCADE, null=True)
    # org_detail = models.ForeignKey(OrgDetail, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.email


class TeacherDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, default=None)
    full_name = models.CharField(max_length=80, default='')
    phone_number = models.CharField(max_length=24, default='')

    def __str__(self):
        return self.full_name


class OrgDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, default=None)
    org_name = models.CharField(max_length=80, default='')
    mobile_number = models.CharField(max_length=24, default='')
    phone_number = models.CharField(max_length=24, default='')
    address = models.CharField(max_length=250, default='')

    def __str__(self):
        return self.org_name


from django.db import models
from django.urls import reverse
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)


# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, reg_no, phone, gender, password=None, is_active=True, is_admin=False,
                    is_staff=False):
        if not first_name or not last_name:
            raise ValueError("Please specify both names")
        if not reg_no:
            raise ValueError("Enter staff/patient reg. number")
        if not phone:
            raise ValueError("User must have phone no")
        if not password:
            raise ValueError("User must specify password")
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            reg_no=reg_no,
            phone=phone,
            gender=gender,
        )
        user.set_password(password)
        user.staff = is_staff
        user.admin = is_admin
        user.active = is_active
        user.save(using=self._db)
        return user

    #admin managers eg IT department,seniors 
    def create_superuser(self, first_name, last_name, reg_no, phone, gender, password=None):
        user = self.create_user(
            first_name,
            last_name,
            reg_no,
            phone,
            gender,
            password=password,
            is_admin=True,
            is_staff=True
        )
        return user

    # staff members eg doctors and nurses
    def create_staff(self, first_name, last_name, reg_no, phone, gender, password=None):
        user = self.create_user(
            first_name,
            last_name,
            reg_no,
            phone,
            gender,
            password=password,
            is_staff=True,
            is_admin=False
        )
        return user


class User(AbstractBaseUser, PermissionsMixin):
    gender_choices = (
        ("Male", 'Male'),
        ('Female', 'Female'),
    )
    #custom user properties 
    first_name = models.CharField(max_length=255, default=None)
    last_name = models.CharField(max_length=255, default=None)
    email = models.EmailField(
        verbose_name='email address', max_length=255, unique=True)
    reg_no = models.CharField(max_length=255, unique=True,
                              help_text='Enter staff/patient reg. number', null=False, default=None)
    phone = models.CharField(max_length=10, unique=True,
                             help_text='must be 10 digits')
    gender = models.CharField(choices=gender_choices,
                              max_length=10, null=True, default=None)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    Objects = UserManager()

    USERNAME_FIELD = 'reg_no'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', 'gender']

    def __str__(self):
        return self.reg_no

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return f'{self.first_name}'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_active(self):
        return self.active

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    def get_absolute_url(self):
        return reverse('/', kwargs={'pk': self.pk})


class Profiles(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, default=None)
    image = models.ImageField()

    def __str__(self):
        return str(self.user)

from django.db import models

# Create your models here.
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager

class MyUserManager(BaseUserManager):
    def create_user(self, email, name, designation, password):
        user = self.model(email=email, name=name, designation=designation, password=password)
        user.set_password(password)
        user.is_staff = True
        user.is_active
        user.is_superuser = False
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, designation, password):
        user = self.create_user(email=email, name=name, designation=designation, password=password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, email_):
        print(email_)
        return self.get(email=email_)


class MyUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100, unique=True)
    designation = models.CharField(max_length=100)
    is_doctor = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    object = MyUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['designation', 'name']

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_short_name(self):
        return self.email

    def natural_key(self):
        return self.email

from django.db import models

# Create your models here.
from django.contrib.auth.models import (
    PermissionsMixin, AbstractBaseUser, BaseUserManager
)
from django.utils import timezone
from safedelete.managers import SafeDeleteManager
from safedelete.models import SafeDeleteModel, NO_DELETE


class MyUserManager(BaseUserManager, SafeDeleteManager):
    def create_user(self, email, name, designation, password, **kwargs):
        now = timezone.local(timezone.now())
        if not email:
            raise ValueError('User must have an email address')
        user = self.model\
            (
                email=self.normalize_email(email),
                name=name,
                designation=designation,
                password=password,
                last_login=now, **kwargs)
        user.set_password(password)
        user.is_superuser = False
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, designation, password, **kwargs):
        user = self.create_user(email=email, name=name, designation=designation, password=password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, email_):
        print(email_)
        return self.get(email=email_)


class MyUser(SafeDeleteModel, AbstractBaseUser):
    _safedelete_policy = NO_DELETE
    RCHOICES = (
        ('doctor', 'Doctor'),
        ('manager', 'Manager'),
        ('helpdesk', 'Helpdesk'),
    )
    email = models.EmailField(verbose_name='email address', unique=True, max_length=255)
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    role = models.CharField(max_length=30, choices=RCHOICES, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = MyUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['designation', 'name']

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def natural_key(self):
        return self.email

    @property
    def is_doctor(self):
        return self.role == 'doctor'

    def is_manager(self):
        return self.role == 'manager'

    def is_helpdesk(self):
        return self.role == 'helpdesk'
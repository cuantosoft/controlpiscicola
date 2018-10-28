from django.db import models


# AbstractBaseUser es mas complicado
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
# probare este https://wsvincent.com/django-custom-user-model-tutorial/
from django.contrib.auth.models import AbstractUser


# class Usuario(AbstractUser):
#     # add additional fields in here
#     JEFE = 'JEFE'
#     TRABAJADOR = 'TRABAJADOR'
#     CARGO_CHOICES = ((JEFE, 'Jefe'), (TRABAJADOR, 'Trabajador'))
#     cargo = models.CharField(max_length=2, choices=CARGO_CHOICES, default=TRABAJADOR);
#
#     def __str__(self):
#         return '{} {}'.format(self.first_name, self.last_name)
#
#



# class User(AbstractBaseUser):
#     finca = models.ForeignKey(Finca)
#     email = models.EmailField(
#         verbose_name='Correo electrónico',
#         max_length=255,
#         unique=True,
#     )
#     # ***************************
#     JEFE = 'JEFE'
# #     TRABAJADOR = 'TRABAJADOR'
# #     CARGO_CHOICES = (
# #         (JEFE, 'Jefe'),
# #         (TRABAJADOR, 'Trabajador'),
# #     )
# #     cargo = models.CharField(max_length=2, choices=CARGO_CHOICES, default=TRABAJADOR,);
#     # ***************************
#     active = models.BooleanField(default=True)
#     staff = models.BooleanField(default=False) # a admin user; non super-user
#     admin = models.BooleanField(default=False) # a superuser
#     # notice the absence of a "Password field", that's built in.
#
#     # USERNAME_FIELD = 'email'
#     # REQUIRED_FIELDS = [] # Email & Password are required by default.
#
#     def get_full_name(self):
#         # The user is identified by their email address
#         return self.email
#
#     def get_short_name(self):
#         # The user is identified by their email address
#         return self.email
#
#     def __str__(self):              # __unicode__ on Python 2
#         return self.email
#
#     def has_perm(self, perm, obj=None):
#         "Does the user have a specific permission?"
#         # Simplest possible answer: Yes, always
#         return True
#
#     def has_module_perms(self, app_label):
#         "Does the user have permissions to view the app `app_label`?"
#         # Simplest possible answer: Yes, always
#         return True
#
#     @property
#     def is_staff(self):
#         "Is the user a member of staff?"
#         return self.staff
#
#     @property
#     def is_admin(self):
#         "Is the user a admin member?"
#         return self.admin
#
#     @property
#     def is_active(self):
#         "Is the user active?"
#         return self.active
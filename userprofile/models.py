from django.db import models
from django.contrib.auth.models import User

# class User(AbstractUser):

#     class Role(models.TextChoices):
#         ADMIN = "ADMIN", 'Admin'
#         STUDENT = "CUSTOMER", 'Customer'
#         VENDOR = "VENDOR", 'Vendor'

#     base_role = Role.ADMIN

#     role = models.CharField(max_length=50, choices=Role.choices)

class Userprofile(models.Model):
    user = models.OneToOneField(User, related_name='userprofile', on_delete=models.CASCADE)
    is_vendor = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

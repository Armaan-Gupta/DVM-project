from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

class Userprofile(models.Model):
    user = models.OneToOneField(User, related_name='userprofile', on_delete=models.CASCADE)
    is_vendor = models.BooleanField(default=False)
    wallet = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username
    
@receiver(post_save, sender=User)
def create_userprofile(sender, instance, created, **kwargs):
    if created:
        Userprofile.objects.create(user=instance, is_vendor=True)

post_save.connect(create_userprofile, sender=get_user_model())




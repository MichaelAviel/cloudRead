from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.



class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='userprofile', on_delete=models.CASCADE)
    # related name helps maintain the relationship with the user model. 
    # One to One maintainse the relationship with the user model.
    wallet_address = models.CharField(max_length=500, null=True, blank=True)
    profile_picture = models.ImageField(null=True, blank=True)
    about = RichTextField(default="", blank=True, null=True)
    # signals to notify when an action occurs. 


@receiver(post_save, sender=User)
def save_profile(sender, instance, created, *args, **kwargs):
    
    print(instance)
    user = instance
    if created:
        profile = UserProfile(user=user)
        profile.save()
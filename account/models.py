from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,
                                on_delete = models.CASCADE, related_name = 'profile')
    profileImage = models.ImageField(upload_to = 'profileImages/',
                                     null = True,
                                     blank = True)
    
    def __str__(self):
        return self.user.first_name
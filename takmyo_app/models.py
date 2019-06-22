from django.db import models
from django.contrib.auth.models import AbstractUser
#from django.contrib.gis.db import models

# Create your models here.
class User(AbstractUser) :
    
    gender = models.CharField(max_length=10, default='unknown')
    postcode = models.CharField(max_length=255, default='unknown')
    address = models.CharField(max_length=255, default='unknown')
    detail_address = models.CharField(max_length=255, default='')
    extra_address = models.CharField(max_length=255, default='')
    phone = models.CharField(max_length=20, default='unknown')
    check_phone = models.BooleanField(default=False)
    is_catsitter = models.BooleanField(default=False)
    is_catee = models.BooleanField(default=False)
    profile_image = models.ImageField(null=True, blank=True, upload_to='profileImage/', default='unknown_icon.png')
    lat = models.FloatField(blank=True, default=0.0)
    lng = models.FloatField(blank=True, default=0.0)

    def __str__(self) :

        return self.username

class Catsitter(models.Model) :

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rate = models.FloatField(blank=True, default=0.0)
    has_pet = models.BooleanField(default=False)
    has_pet_experience = models.BooleanField(default=False)
    available_pill = models.BooleanField(default=False)
    available_identification = models.BooleanField(default=False)
    available_visit = models.BooleanField(default=False)
    available_consignment = models.BooleanField(default=False)


class Notification(models.Model) :

    CATEGORY_CHOICES = {
        ('review', 'Review'),
        ('form', 'Form')
    }

    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, 
                                on_delete = models.CASCADE, 
                                null=True, 
                                blank=True, 
                                related_name='create_notifications')
    receiver = models.ForeignKey(User, 
                                on_delete = models.CASCADE, 
                                null=True, 
                                blank=True, 
                                related_name='receive_notifications')
    content = models.TextField()
    category = models.CharField(max_length = 30, choices=CATEGORY_CHOICES, null=True)
    is_checked = models.BooleanField(default=False)



    def __str__(self) :

        return self.creator.username + ' - ' + self.receiver.username + ' - ' + self.category 


    class Meta :

        ordering = ['-created_at']
    
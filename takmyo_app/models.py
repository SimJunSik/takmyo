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

    PLACE_CHOICES = {
        ('visit', 'Visit'),
        ('consignment', 'Consignment'),
        ('both', 'Both')
    }

    TIME_CHOICES = {
        ('am', 'Am'),
        ('pm', 'Pm'),
        ('both', 'Both')
    }

    DAY_CHOICES = {
        ('weekday', 'Weekday'),
        ('weekend', 'Weekend'),
        ('both', 'Both')
    }

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    name = models.CharField(max_length = 100, default="unknown")
    catsitter_profile_image = models.ImageField(upload_to='catsitter_profileImage/', default='unknown_icon.png')
    rate_per_hundred = models.FloatField(blank=True, default=0.0)
    rate_per_five = models.FloatField(blank=True, default=0.0)
    have_pet = models.BooleanField(default=False)
    have_pet_experience = models.BooleanField(default=False)
    have_care_experience = models.BooleanField(default=False)
    available_pill = models.BooleanField(default=False)
    available_identification = models.BooleanField(default=False)
    available_place = models.CharField(max_length=10, choices=PLACE_CHOICES, default='')

    visit_price_per_once = models.IntegerField(default=0)
    visit_price_per_extra_cat = models.IntegerField(default=0)

    consignment_price_per_one_day = models.IntegerField(default=0)
    consignment_price_per_one_week = models.IntegerField(default=0)
    consignment_price_per_one_month = models.IntegerField(default=0)
    consignment_price_per_extra_cat = models.IntegerField(default=0)

    register_date = models.DateTimeField(auto_now_add=True)

    available_day = models.CharField(max_length=10, choices=DAY_CHOICES, default='')

    available_weekday_time = models.CharField(max_length=10, choices=TIME_CHOICES, default='')
    available_weekend_time = models.CharField(max_length=10, choices=TIME_CHOICES, default='')

    introduce = models.TextField(default="")

    warning = models.TextField(default="")

    available_region = models.TextField(default="")

    activation = models.BooleanField(default=False)

    def __str__(self) :

        return self.user.username


    class Meta :

        ordering = ['-register_date']


class Catsitter_promotion_image(models.Model) :
    
    catsitter = models.ForeignKey(Catsitter, on_delete=models.CASCADE, related_name='catsitter_promotion_image')
    promotion_image = models.ImageField(upload_to='catsitter_promotionImage/', default='unknown_icon.png')

    def __str__(self) :

        return self.catsitter.user.username

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
    
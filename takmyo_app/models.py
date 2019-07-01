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
    rate_per_hundred = models.DecimalField(blank=True, default=0.0, max_digits=5, decimal_places=1)
    rate_per_five = models.DecimalField(blank=True, default=0.0, max_digits=5, decimal_places=1)
    have_pet = models.BooleanField(default=False)
    have_pet_experience = models.BooleanField(default=False)
    have_care_experience = models.BooleanField(default=False)
    available_pill = models.BooleanField(default=False)
    available_identification = models.BooleanField(default=False)
    available_place = models.CharField(max_length=20, choices=PLACE_CHOICES, default='')

    visit_price_per_once = models.IntegerField(default=0)
    visit_price_per_extra_cat = models.IntegerField(default=0)
    available_change_visit_price_per_extra_cat = models.BooleanField(default=False)

    consignment_price_per_one_day = models.IntegerField(default=0)
    consignment_price_per_one_week = models.IntegerField(default=0)
    consignment_price_per_one_month = models.IntegerField(default=0)
    consignment_price_per_extra_cat = models.IntegerField(default=0)
    available_change_consignment_price_per_extra_cat = models.BooleanField(default=False)

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


    @property
    def get_reviews_num(self) :

        return self.catsitter_reviews.all().count()


class Catee(models.Model) :

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length = 100, default="unknown")
    register_date = models.DateTimeField(auto_now_add=True)
    catee_profile_image = models.ImageField(upload_to='catee_profileImage/', default='unknown_icon.png')

    def __str__(self) :

        return self.name

    @property
    def get_cats_num(self) :

        return self.catee_cats.all().count()

class Cat(models.Model) :

    owner = models.ForeignKey(Catee, on_delete=models.CASCADE, related_name='catee_cats')
    cat_profile_image = models.ImageField(upload_to='cat_profileImage/' + str(owner.name) + '/', 
                                            default='unknown_icon.png',
                                            null=True,
                                            blank=True)
    name = models.CharField(max_length=50, default='unknown')
    age = models.CharField(max_length=50, default='unknown')
    breed = models.CharField(max_length=50, default='unknown')
    gender = models.CharField(max_length=20, default='unknown')
    neutralization = models.BooleanField(default=False)
    hospital = models.CharField(max_length=200, default='unknown')
    warning = models.TextField()

    def __str__(self) :

        return self.owner.name + ' - ' + self.name


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

class CatsitterReview(models.Model) :

    catee = models.ForeignKey(Catee, 
                                on_delete = models.CASCADE,
                                null=True,
                                related_name='catee_reviews')

    catsitter = models.ForeignKey(Catsitter, 
                                on_delete = models.CASCADE,
                                null=True,
                                related_name='catsitter_reviews')

    content = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    time_rate = models.FloatField(default=0.0)
    kindness_rate = models.FloatField(default=0.0)
    achievement_rate = models.FloatField(default=0.0)
    total_rate = models.FloatField(default=0.0)
    total_rate_per_hundred = models.IntegerField(default=0)

    def __str__(self) :

        return self.catsitter.name + ' - ' + self.content

    class Meta :

        ordering = ['-created_at']

class CatsitterExperienceImage(models.Model) :

    catsitter = models.ForeignKey(Catsitter, 
                                on_delete = models.CASCADE, 
                                null=True, 
                                blank=True, 
                                related_name='catsitter_experience_images')

    catsitter_experience_image = models.ImageField(upload_to='catsitter_experienceImage/', default='unknown_icon.png')
    caption = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) :

        return self.catsitter.name + ' - ' + self.id

    class Meta :

        ordering = ['-created_at']

class CateeToCatsitterForm(models.Model) :

    PLACE_CHOICES = {
        ('visit', 'Visit'),
        ('consignment', 'Consignment')
    }

    STATE_CHOICES = {
        ('recognized', 'Recognized'),
        ('progress', 'Progress'),
        ('unrecognized', 'Unrecognized')
    }

    catee = models.ForeignKey(Catee, on_delete=models.CASCADE, related_name='from_catee_form')
    catsitter = models.ForeignKey(Catsitter, on_delete=models.CASCADE, related_name='to_catsitter_form')
    
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now_add=True)

    place = models.CharField(max_length=20, choices=PLACE_CHOICES, default='')

    condition = models.TextField(default='', null=True, blank=True)

    comment = models.TextField(default='', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    state = models.CharField(max_length=50, choices=STATE_CHOICES, default='')

    def __str__(self) :

        return self.catee.name + ' - ' + self.catsitter.name

    class Meta :

        ordering = ['-created_at']
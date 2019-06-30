from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Notification)
admin.site.register(Catsitter)
admin.site.register(Catee)
admin.site.register(Cat)
admin.site.register(Catsitter_promotion_image)
admin.site.register(CatsitterReview)
admin.site.register(CatsitterExperienceImage)
admin.site.register(CateeToCatsitterForm)

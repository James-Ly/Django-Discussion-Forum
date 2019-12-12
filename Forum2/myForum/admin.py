from django.contrib import admin
from myForum import models

# Register your models here.

admin.site.register(models.UserProfile)
admin.site.register(models.Section)
admin.site.register(models.SubSection)
admin.site.register(models.Posts)

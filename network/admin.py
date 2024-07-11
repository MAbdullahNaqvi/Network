from django.contrib import admin
from .models import User, posts, Userprofile

admin.site.register(User)
admin.site.register(posts)
admin.site.register(Userprofile)

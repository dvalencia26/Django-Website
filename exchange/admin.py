from django.contrib import admin
from .models import *

admin.site.register(Article)
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(Country)
admin.site.register(Tags)
admin.site.register(Thread)


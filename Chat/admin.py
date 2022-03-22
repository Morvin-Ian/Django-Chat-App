from django.contrib import admin
from .models import *

admin.site.register(ChatRoom)
admin.site.register(Message)
admin.site.register(Topic)
admin.site.register(Profile)
from django.contrib import admin
from .models import User, Message, Token
# Register your models here.
admin.site.register([User, Message, Token])
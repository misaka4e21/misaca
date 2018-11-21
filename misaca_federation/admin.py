from django.contrib import admin
from .models import Account, User, Status

# Register your models here.
admin.site.register(Account)
admin.site.register(User)

# Status
admin.site.register(Status)
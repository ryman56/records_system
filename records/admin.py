from django.contrib import admin

# Register your models here.
from .models import Department, Record, User

admin.site.register(Department)
admin.site.register(Record)
admin.site.register(User)

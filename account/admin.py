from django.contrib import admin
from .models import Profile
# Register your models here.

@admin.register(Profile)
class PofileAdmin(admin.ModelAdmin):
    list_display = ('gender',)

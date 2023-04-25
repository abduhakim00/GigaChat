from django.contrib import admin
from . import models


@admin.register(models.Member)
class MemberAdmin(admin.ModelAdmin):
    list_display=['user', 'avatar']

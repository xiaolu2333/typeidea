from django.contrib import admin
from .models import *
from typeidea.base_admin import BaseOwnerAdmin


# Register your models here.
@admin.register(Link)
class LinkAdmin(BaseOwnerAdmin):
    list_display = ['title', 'href', 'status', 'weight', 'created_time']
    fields = ['title', 'href', 'weight']


@admin.register(SideBar)
class SideBarAdmin(BaseOwnerAdmin):
    list_display = ['title', 'display_type', 'content', 'created_time']
    fields = ['title', 'display_type', 'content']
from django.contrib import admin
from .models import *
import time


# Register your models here.
@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ['title', 'href', 'status', 'weight', 'created_time']
    fields = ['title', 'href', 'weight']

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        localtime = time.asctime(time.localtime(time.time()))
        try:
            Link_old = self.model.objects.filter(id=obj.pk)
        except:
            Link_old = "👨‍🍳初始信息"
        cLink_new = form.cleaned_data
        f = open("/home/dfl/py-projects/web/django/log.txt", "a")
        f.write(
            "Category" + str(Link_old) + "在" + localtime + "被" + str(obj.owner) + "修改为" + str(Link_new) + '\r\n')
        return super(LinkAdmin, self).save_model(request, obj, form, change)


@admin.register(SideBar)
class SideBarAdmin(admin.ModelAdmin):
    list_display = ['title', 'display_type', 'content', 'created_time']
    fields = ['title', 'display_type', 'content']

    def save_model(self, request, obj, form, change):
        if change:
            obj.owner = request.user
            localtime = time.asctime(time.localtime(time.time()))
            try:
                SideBar_old = self.model.objects.filter(id=obj.pk)
            except:
                SideBar_old = "👨‍🍳初始信息"
            SideBar_new = form.cleaned_data
            f = open("/home/dfl/py-projects/web/django/log.txt", "a")
            f.write(
                "Category" + str(SideBar_old) + "在" + localtime + "被" + str(obj.owner) + "修改为" + str(SideBar_new) + '\r\n')
            return super(SideBarAdmin, self).save_model(request, obj, form, change)

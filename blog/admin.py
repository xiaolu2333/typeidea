from django.contrib import admin
from .models import Post, Tag, Category
import time


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'is_nav', 'created_time', 'owner')
    fields = ('name', 'status', 'is_nav')

    def save_model(self, request, obj, form, change):
        if change:
            obj.owner = request.user
            localtime = time.asctime(time.localtime(time.time()))
            category_old = self.model.objects.get(pk=obj.pk).name
            category_new = form.cleaned_data['name']
            f = open("/home/dfl/py-projects/web/django/log.txt", "a")
            f.write(str(category_old) + "在" + localtime + "被" + str(obj.owner) + "修改为" + str(category_new) + '\r\n')
            return super(CategoryAdmin, self).save_model(request, obj, form, change)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')

    def save_model(self, request, obj, form, change):
        if change:
            obj.owner = request.user
            localtime = time.asctime(time.localtime(time.time()))
            category_old = self.model.objects.get(pk=obj.pk).name
            category_new = form.cleaned_data['name']
            f = open("/home/dfl/py-projects/web/django/log.txt", "a")
            f.write(str(category_old) + "在" + localtime + "被" + str(obj.owner) + "修改为" + str(category_new) + '\r\n')
            return super(TagAdmin, self).save_model(request, obj, form, change)

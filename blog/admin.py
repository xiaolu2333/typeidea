from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

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
            try:
                category_old = self.model.objects.get(name=obj.name).name
            except:
                category_old = "👨‍🍳初始信息"
            category_new = form.cleaned_data['name']
            f = open("/home/dfl/py-projects/web/django/log.txt", "a")
            f.write("Category" + str(category_old) + "在" + localtime + "被" + str(obj.owner) + "修改为" + str(category_new) + '\r\n')
            return super(CategoryAdmin, self).save_model(request, obj, form, change)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_time', 'owner')
    fields = ('name', 'status')

    def save_model(self, request, obj, form, change):
        if change:
            obj.owner = request.user
            localtime = time.asctime(time.localtime(time.time()))
            try:
                tag_old = self.model.objects.get(name=obj.name).name
            except:
                tag_old = "👨‍🍳初始信息"
            tag_new = form.cleaned_data['name']
            f = open("/home/dfl/py-projects/web/django/log.txt", "a")
            f.write("Tag" + str(tag_old) + "在" + localtime + "被" + str(obj.owner) + "修改为" + str(tag_new) + '\r\n')
            return super(TagAdmin, self).save_model(request, obj, form, change)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'created_time', 'operator']
    list_display_links = []

    list_filter = ['category']
    search_fields = ['title', 'category__name']

    actions_on_bottom = True

    fields = [('title', 'category'),
              'desc', 'status', 'tag', 'content']

    def operator(self, obj):
        return format_html(
            '<a href={}>编辑</a>',
            reverse('admin:blog_post_change', args=(obj.id,))
        )

    operator.short_description = "操作"

    def save_model(self, request, obj, form, change):
        if change:
            obj.owner = request.user
            localtime = time.asctime(time.localtime(time.time()))
            try:
                post_old = self.model.objects.filter(id=obj.pk)
            except:
                post_old = "👨‍🍳初始信息"
            post_new = form.cleaned_data
            f = open("/home/dfl/py-projects/web/django/log.txt", "a")
            f.write("Post" + str(post_old) + "在" + localtime + "被" + str(obj.owner) + "修改为" + str(post_new) + '\r\n')
            return super(PostAdmin, self).save_model(request, obj, form, change)
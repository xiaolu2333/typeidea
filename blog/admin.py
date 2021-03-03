from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Post, Tag, Category
import time
from .adminforms import PostAdminForm


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'is_nav', 'created_time', 'owner', 'post_count')
    fields = ('name', 'status', 'is_nav')

    # list_filter = [CategoryOwnerFilter, ]

    def post_count(self, obj):
        return obj.post_set.count()
    post_count.short_description = "文章数量"

    def save_model(self, request, obj, form, change):
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


class CategoryOwnerFilter(admin.SimpleListFilter):
    title = "分类过滤器"
    parameter_name = "owner_category"

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ['title', 'category', 'status', 'created_time', 'owner', 'operator']
    list_display_links = []

    list_filter = [CategoryOwnerFilter, ]
    search_fields = ['title', 'category__name']

    actions_on_top = True

    fieldsets = (
        ("基本配置", {
            "description": "基本配置描述",
            "fields": (
                ('title', 'category'),
                'status'
            )
        }),
        ("内容", {
            "fields": (
                'desc', 'content'
            )
        }),
        ("额外信息", {
            "classes": ("collapse",),
            "fields": (
                'tag',
            )
        })
    )

    filter_horizontal = ("tag",)

    def operator(self, obj):
        return format_html(
            '<a href={}>编辑</a>',
            reverse('admin:blog_post_change', args=(obj.id,))
        )
    operator.short_description = "操作"

    def save_model(self, request, obj, form, change):
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

    def get_queryset(self, request):
        qs = super(PostAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)

    class Media:
        css = {
            'all': ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css',),
        }
        js = ('https://cdn.bootcss.com/bootstrap/4.0 0-beta.2/js/bootstrap.bundle.js',)
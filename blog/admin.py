from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Post, Tag, Category
import time
from .adminforms import PostAdminForm
from typeidea.custom_site import custom_site


# Register your models here.
admin.site.site_title = "博客系统后台管理"
admin.site.site_header = "博客——记录每一段成长"


class PostInline(admin.TabularInline):
    fields = ("title", "desc")
    extra = 1
    model = Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [PostInline, ]

    list_display = ('name', 'status', 'is_nav', 'created_time', 'owner', 'post_count')
    fields = ('name', 'status', 'is_nav')

    def post_count(self, obj):
        return obj.post_set.count()
    post_count.short_description = "文章数量"

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        localtime = time.asctime(time.localtime(time.time()))
        category_old = self.model.objects.get(name=obj.name).name
        if not category_old:
            category_old = "👨‍🍳初始信息"
        category_new = form.cleaned_data['name']
        f = open("/home/dfl/py-projects/web/django/log.txt", "a")
        f.write("Category" + str(category_old) + "在" + localtime + "被" + str(obj.owner) + "修改为" + str(category_new) + '\r\n')
        return super(CategoryAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super(CategoryAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_time', 'owner')
    fields = ('name', 'status')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        localtime = time.asctime(time.localtime(time.time()))
        tag_old = self.model.objects.get(name=obj.name).name
        if not tag_old:
            tag_old = "👨‍🍳初始信息"
        tag_new = form.cleaned_data['name']
        f = open("/home/dfl/py-projects/web/django/log.txt", "a")
        f.write("Tag" + str(tag_old) + "在" + localtime + "被" + str(obj.owner) + "修改为" + str(tag_new) + '\r\n')
        return super(TagAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super(TagAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)


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


class TagOwnerFilter(admin.SimpleListFilter):
    title = "标签过滤器"
    parameter_name = "owner_tag"

    def lookups(self, request, model_admin):
        return Tag.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        tag_id = self.value()
        if tag_id:
            return queryset.filter(tag=self.value())


@admin.register(Post, site=custom_site)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ['title', 'category', 'colored_status', 'created_time', 'owner', 'operator']
    list_display_links = []

    list_filter = [CategoryOwnerFilter, TagOwnerFilter]
    search_fields = ['title', 'category__name']

    actions_on_top = True

    fieldsets = (
        ("基本配置", {
            "description": "基本配置描述",
            "fields": (
                ('title', 'category',),
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
                "tag",
            )
        })
    )

    filter_horizontal = ("tag",)

    def operator(self, obj):
        return format_html(
            '<a href={}>编辑</a>',
            reverse('cus_admin:blog_post_change', args=(obj.id,))
        )
    operator.short_description = "操作"

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        localtime = time.asctime(time.localtime(time.time()))
        post_old = self.model.objects.filter(id=obj.pk)
        if not post_old:
            post_old = "👨‍🍳初始信息"
        post_new = form.cleaned_data
        f = open("/home/dfl/py-projects/web/django/log.txt", "a")
        f.write("Post" + str(post_old) + "在" + localtime + "被" + str(obj.owner) + "修改为" + str(post_new) + '\r\n')
        return super(PostAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super(PostAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            kwargs["queryset"] = Category.objects.filter(owner=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "tag":
            kwargs["queryset"] = Tag.objects.filter(owner=request.user)
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    # 会导致文章修改页面的“额外信息”在classes设置为collapse时显示失败
    # class Media:
    #     css = {
    #         'all': ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css',),
    #     }
    #     js = ('https://cdn.bootcss.com/bootstrap/4.0 0-beta.2/js/bootstrap.bundle.js',)
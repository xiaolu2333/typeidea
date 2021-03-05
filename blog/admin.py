from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.admin.models import LogEntry

from .models import Post, Tag, Category
from .adminforms import PostAdminForm
from typeidea.custom_site import custom_site
from typeidea.base_admin import BaseOwnerAdmin

# Register your models here.
admin.site.site_title = "博客系统后台管理"
admin.site.site_header = "博客——记录每一段成长"


class PostInline(admin.TabularInline):
    fields = ("title", "desc")
    extra = 1
    model = Post


@admin.register(Category)
class CategoryAdmin(BaseOwnerAdmin):
    inlines = [PostInline, ]

    list_display = ('name', 'status', 'is_nav', 'created_time', 'owner', 'post_count')
    fields = ('name', 'status', 'is_nav')

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = "文章数量"


@admin.register(Tag)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time', 'owner')
    fields = ('name', 'status')


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
class PostAdmin(BaseOwnerAdmin):
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

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            kwargs["queryset"] = Category.objects.filter(owner=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "tag":
            kwargs["queryset"] = Tag.objects.filter(owner=request.user)
        return super().formfield_for_manytomany(db_field, request, **kwargs)


@admin.register(LogEntry, site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['object_repr', 'object_id', 'action_flag', 'user', 'change_message']
from django.utils.html import format_html
from django.contrib.auth.models import User
from django.db import models
from django.utils.functional import cached_property
import mistune


# Create your models here.
class Category(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除')
    )

    name = models.CharField(max_length=50, verbose_name="名称")
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")
    is_nav = models.BooleanField(default=False, verbose_name="是否为导航")
    owner = models.ForeignKey(User, verbose_name="作者", on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    @classmethod
    def get_navs(cls, owner=None):
        if owner:
            categories = Category.objects.filter(status=Category.STATUS_NORMAL, owner=owner)
        else:
            categories = Category.objects.filter(status=Category.STATUS_NORMAL)
        nav_categories = []
        normal_categories = []
        for cate in categories:
            if cate.is_nav:
                nav_categories.append(cate)
            else:
                normal_categories.append(cate)

        return {
            'navs': nav_categories,
            'categories': normal_categories
        }

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = "分类"


class Tag(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除')
    )

    name = models.CharField(max_length=50, verbose_name="名称")
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")
    owner = models.ForeignKey(User, verbose_name="作者", on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = "标签"
        indexes = [
            models.Index(fields=['id'], name='tag_id_idx'),
        ]


class Post(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
        (STATUS_DRAFT, '草稿')
    )

    title = models.CharField(max_length=255, verbose_name="标题")
    desc = models.CharField(max_length=1024, blank=True, verbose_name="摘要")
    content = models.TextField(verbose_name="正文", help_text="正丈必须为 MarkDown 格式！")
    content_html = models.TextField(verbose_name="正文HTML代码", blank=True, editable=False)
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")
    category = models.ForeignKey(Category, verbose_name="分类", on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag, verbose_name="标签")
    owner = models.ForeignKey(User, verbose_name="作者", on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    is_md = models.BooleanField(default=False, verbose_name="正文markdown吾法")   # 默认使用ckeditor
    pv = models.PositiveIntegerField(default=1)
    uv = models.PositiveIntegerField(default=1)

    def colored_status(self):
        if self.status == 0:
            color_code = 'red'
        elif self.status == 1:
            color_code = 'green'
        else:
            color_code = 'yellow'
        return format_html(
            '<span style="color:{};">{}</span>',
            color_code, self.status,
        )

    colored_status.short_description = '文章状态'

    @staticmethod
    def get_by_tag(tag_id):
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            tag = None
            post_list = []
        else:
            post_list = tag.post_set.filter(status=Post.STATUS_NORMAL).select_related("owner", "category")

        return post_list, tag

    @staticmethod
    def get_by_category(category_id, owner_id=None):
        try:
            if owner_id:
                category = Category.objects.get(id=category_id, owner_id=owner_id, status=Post.STATUS_NORMAL).order_by("-id")
            else:
                category = Category.objects.get(id=category_id, status=Post.STATUS_NORMAL).order_by("-id")
        except Category.DoesNotExist:
            category = None
            post_list = []
        else:
            post_list = category.post_set.filter(status=Post.STATUS_NORMAL).select_related("owner", "category")

        return post_list, category

    @classmethod
    def latest_posts(cls, owner_id=None, with_related=True):
        queryset = cls.objects.filter(status=cls.STATUS_NORMAL)
        if owner_id:
            queryset = queryset.filter(owner=owner_id)
        if with_related:
            defer_fields = ['content', 'content_html']
            queryset = queryset.prefetch_related('owner', 'category', 'tag').defer(*defer_fields)
        return queryset

    @classmethod
    def hot_posts(cls, owner_id=None, with_related=True):
        queryset = cls.objects.filter(status=cls.STATUS_NORMAL)
        if owner_id:
            queryset = queryset.filter(owner=owner_id)
        if with_related:
            defer_fields = ['content','content_html']
            queryset = queryset.prefetch_related ('owner','category','tag').defer(*defer_fields)
        return queryset.order_by('-pv')

    @cached_property
    def tags(self):
        return ', '.join(self.tag.values_list('name', flat=True))

    def save(self, *args, **kwargs):
        if self.is_md:
            self.content_html = mistune.markdown(self.content)
        else:
            self.content_html = self.content
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = verbose_name_plural = "文章"
        # 配合分页，进行排序
        ordering = ['-id']
        indexes = [
            models.Index(fields=['id'], name='post_id_idx'),
        ]

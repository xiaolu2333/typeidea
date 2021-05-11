from datetime import date

from django.db.models import Q, F
from django.views.generic import DetailView, ListView
from django.shortcuts import get_object_or_404
from blog.models import Tag, Category, Post
from config.models import SideBar
from django.core.cache import cache


# Create your views here.
class CommonViewMixin(object):
    def setup(self, request, *args, **kwargs):
        """Initialize attributes shared by all view methods."""
        if hasattr(self, 'get') and not hasattr(self, 'head'):
            self.head = self.get
        self.request = request
        self.args = args
        self.kwargs = kwargs

    def get_context_data(self, **kwargs):
        context = super(CommonViewMixin, self).get_context_data(**kwargs)
        context.update({
            'sidebars': SideBar.get_all(),
            'user': self.request.user
        })
        if self.request.method == 'GET':
            context.update(Category.get_navs(owner=self.request.user.id))
        return context


class IndexView(CommonViewMixin, ListView):
    queryset = Post.latest_posts()
    paginate_by = 2
    context_object_name = 'post_list'
    template_name = 'blog/list.html'


class CategoryView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, pk=category_id)
        context.update({
            'category': category,
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)


class TagView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Tag, pk=tag_id)
        context.update({
            'tag': tag,
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tag=tag_id)


class PostDetailView(CommonViewMixin, DetailView):
    queryset = Post.latest_posts()
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        self.handle_visited()
        return response

    def handle_visited(self):
        increase_pv = False
        uid = self.request.uid  # 获取middleware中设置的用户id
        pv_key = 'pv:%s:%s' % (uid, self.request.path)

        if not cache.get(pv_key):
            increase_pv = True
            cache.set(pv_key, 1, 1 * 60)  # 1分钟有效，防止统计1分钟内多次刷新的情况
        if increase_pv:
            Post.objects.filter(pk=self.object.id).update(pv=F('pv') + 1)


class SearchView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({
            'keyword': self.request.GET.get('keyword', '')
        })
        return context

    def get_queryset(self):
        type_id = self.kwargs.get('type_id')
        if type_id == 1:
            # search personal
            self.queryset = Post.latest_posts(owner_id=self.request.user.id)
        keyword = self.request.GET.get('keyword', '').strip()
        if not keyword:
            return self.queryset
        return self.queryset.filter(Q(title__contains=keyword) | Q(desc__contains=keyword))


class AuthorView(IndexView):
    def get_queryset(self):
        queryset = super().get_queryset()
        author_id = self.kwargs.get('author_id')
        return queryset.filter(owner=author_id)


class MyPostsView(CommonViewMixin, ListView):
    paginate_by = 2
    context_object_name = 'post_list'
    template_name = 'blog/list.html'

    def get_queryset(self):
        queryset = Post.latest_posts(owner_id=self.request.user.id)
        return queryset

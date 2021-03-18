from django.shortcuts import render
from blog.models import Tag, Category, Post
from config.models import SideBar
from django.views.generic import DetailView, ListView


# Create your views here.
# def post_list(request, category_id=None, tag_id=None):
#     tag = None
#     category = None
#
#     if tag_id:
#         post_list, tag = Post.get_by_tag(tag_id)
#     elif category_id:
#         post_list, category = Post.get_by_category(category_id)
#     else:
#         post_list = Post.latest_posts()
#
#     context = {
#         'category': category,
#         'tag': tag,
#         'post_list': post_list,
#         'sidebars': SideBar.get_all(),
#     }
#     context.update(Category.get_navs(owner=request.user))
#
#     return render(request, 'list.html', context=context)
#

class PostListView(ListView):
    queryset = Post.latest_posts()
    paginate_by = 1
    context_object_name = 'post_list'
    template_name = 'list.html'


class PostDetailView(DetailView):
    model = Post
    template_name = 'detail.html'
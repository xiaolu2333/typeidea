"""typeidea URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps import views as sitemap_views
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls

from blog.views import IndexView, CategoryView, TagView, PostDetailView, SearchView, AuthorView, MyPostsView
from config.views import LinkListView
from .custom_site import custom_site
from comment.views import CommentView
from blog.rss import LatestPostFeed
from blog.sitemap import PostSitemap
from blog.apis import PostViewSet, CategoryViewSet, TagViewSet

routers = DefaultRouter()
routers.register('post', PostViewSet, basename='api-post')
routers.register('category', CategoryViewSet, basename='api-category')
routers.register('tag', TagViewSet, basename='api-tag')

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('myposts/', MyPostsView.as_view(), name="my_posts"),
    path('post/<int:post_id>.html', PostDetailView.as_view(), name="post_detail"),
    path('category/<int:category_id>', CategoryView.as_view(), name="category_list"),
    path('tag/<int:tag_id>', TagView.as_view(), name="tag_list"),
    path('links/', LinkListView.as_view(), name="links"),
    path('search/<int:type_id>', SearchView.as_view(), name='search'),
    path('author/<int:author_id>', AuthorView.as_view(), name='author'),
    path('comment/', CommentView.as_view(), name='comment'),
    path('ckeditor/', include('ckeditor_uploader.urls')),

    path('rss/', LatestPostFeed(), name='rss'),
    path('sitemap.xml/', sitemap_views.sitemap, {'sitemaps': {'posts': PostSitemap}}, name='sitemap'),

    path('super_admin/', admin.site.urls, name="super_admin"),
    path('admin/', custom_site.urls, name="admin"),

    path('api/', include((routers.urls, 'blog'), namespace='api-post')),
    path('api/docs/', include_docs_urls(title='API document')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns.append(path('__debug__/', include(debug_toolbar.urls)))

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from blog.models import Post,Category
from blog.serializers import (
    PostSerializer, PostDetailSerializer,
    CategorySerializer,CategoryDetailSerializer
)


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list:
    返回博文列表数据

    retrieve:
    返回博文详情数据
    """
    queryset = Post.objects.filter(status=Post.STATUS_NORMAL)
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = PostDetailSerializer
        return super().retrieve(request, *args, **kwargs)
    # 获取某分类下的文章类表
    # def filter_queryset(self, queryset):
    #     category_id = self.request.query_params.get('category')
    #     if category_id:
    #         queryset = queryset.filter(category_id=category_id)
    #     return queryset


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(status=Category.STATUS_NORMAL)

    # 获取某分类下的文章类表
    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = CategoryDetailSerializer
        return super().retrieve(request, *args, **kwargs)

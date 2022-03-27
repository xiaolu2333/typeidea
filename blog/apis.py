from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from blog.models import Post
from blog.serializers import PostSerializer, PostDetailSerializer


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
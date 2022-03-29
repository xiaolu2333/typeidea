from rest_framework import serializers, pagination

from blog.models import Post, Category, Tag


class PostSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )
    tag = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )
    owner = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    created_time = serializers.DateTimeField(
        format="%Y-%m-%d %H-%M-%S"
    )

    class Meta:
        model = Post
        fields = ['id', 'title', 'category', 'tag', 'owner', 'desc', 'created_time']


class PostDetailSerializer(PostSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'category', 'tag', 'owner', 'desc', 'content_html', 'created_time']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'created_time']


class CategoryDetailSerializer(CategorySerializer):
    posts = serializers.SerializerMethodField('paginated_posts')  # SerializerMethodField将paginated_posts方法的结果反向关联到posts

    class Meta:
        model = Category
        fields = ['id', 'name', 'created_time', 'posts']

    # 反向获取某类下的文章类表
    def paginated_posts(self, obj):
        posts = obj.post_set.filter(status=Post.STATUS_NORMAL)  # 本质是一个反向过滤查询
        paginator = pagination.PageNumberPagination()   # 需要手动做分页
        page = paginator.paginate_queryset(posts, self.context['request'])
        serializer = PostSerializer(page, many=True, context={'request': self.context['request']})
        return {
            'count': posts.count(),
            'results': serializer.data,
            'previous': paginator.get_previous_link(),
            'next': paginator.get_next_link()
        }


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'created_time']

class TagDetailSerializer(CategorySerializer):
    posts = serializers.SerializerMethodField('paginated_posts')  # SerializerMethodField将paginated_posts方法的结果反向关联到posts

    class Meta:
        model = Category
        fields = ['id', 'name', 'created_time', 'posts']

    # 反向获取某类下的文章类表
    def paginated_posts(self, obj):
        posts = obj.post_set.filter(status=Post.STATUS_NORMAL)  # 本质是一个反向过滤查询
        paginator = pagination.PageNumberPagination()   # 需要手动做分页
        page = paginator.paginate_queryset(posts, self.context['request'])
        serializer = PostSerializer(page, many=True, context={'request': self.context['request']})
        return {
            'count': posts.count(),
            'results': serializer.data,
            'previous': paginator.get_previous_link(),
            'next': paginator.get_next_link()
        }
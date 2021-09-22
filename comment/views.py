from django.shortcuts import redirect
from django.views.generic import TemplateView

from comment.forms import CommentForm
from blog.models import Post


# Create your views here.
class CommentView(TemplateView):
    http_method_names = ['post']
    template_name = "comment/result.html"

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST)
        target = request.POST.get('target')
        target_type = target.split('/')[1]
        temp = None
        if target_type == 'post':
            target_id = target.split('/')[-1].split('.')[0]
            temp = Post.objects.get(id=target_id).title # 获取文章标题
        if target_type == 'links':
            temp = '友链页面'

        if comment_form.is_valid():
            instance = comment_form.save(commit=False)
            instance.target = temp
            instance.save()
            succeed = True
            return redirect(target)
        else:
            succeed = False
        target = temp
        context = {
            'succeed': succeed,
            'form': comment_form,
            'target': target
        }
        return self.render_to_response(context=context)
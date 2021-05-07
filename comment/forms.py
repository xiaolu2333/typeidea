from django import forms
from django.utils.safestring import mark_safe

from comment.models import Comment


class CommentForm(forms.ModelForm):
    nickname = forms.CharField(
        label="昵称",
        max_length=50,
        widget=forms.widgets.Input(
            attrs={'class': 'form_control', 'style': 'width: 90%;'}
        )
    )
    email = forms.EmailField(
        label="邮箱",
        max_length=50
    )
    website = forms.CharField(
        label="网站",
        max_length=100,
        widget=forms.widgets.URLInput(
            attrs={'class': 'form-control', 'style': 'width: 90%;'}
        )
    )
    content = forms.CharField(
        label="内容",
        max_length=500,
        widget=forms.widgets.Textarea(
            attrs={'class': 'form-control', 'rows': 3, 'clos': 10}
        )
    )

    # 这是更灵活的设置CSS属性的办法
    email.widget.attrs.update({'class': 'form-control', 'style': 'width: 90%;'})

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) < 10:
            raise forms.ValidationError("评论内容要大于10字符哦～")
        return content

    class Meta:
        model = Comment
        fields = ['nickname', 'email', 'website', 'content']

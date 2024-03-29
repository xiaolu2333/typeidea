from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from blog.models import Post


class PostAdminForm(forms.ModelForm):
    desc = forms.CharField(widget=forms.Textarea, label="摘要", required=True)
    content_ck = forms.CharField(widget=CKEditorUploadingWidget, label="富文本正文", required=False)
    content_md = forms.CharField(widget=forms.Textarea, label="markdown正文", required=False)
    content = forms.CharField(widget=forms.HiddenInput, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.is_md:
            self.fields['content_md'].initial = self.instance.content
        else:
            self.fields['content_ck'].initial = self.instance.content

    def clean(self):
        is_md = self.cleaned_data.get('is_md')
        if is_md:
            content_field_name = 'content_md'
        else:
            content_field_name = 'content_ck'
        content = self.cleaned_data.get(content_field_name)
        if not content:
            self.add_error(content_field_name, '内容为必填项！')
        self.cleaned_data['content'] = content
        return super(PostAdminForm, self).clean()

    class Media:
        js = (
            'js/post_editor.js',
        )

    class Meta:
        model = Post
        fields = ('category', 'tag', 'desc', 'title', 'is_md','content_md', 'content_ck', 'status')

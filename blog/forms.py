from django import forms

from .models import Post,Comment


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)

class CommentForm(forms.ModelForm):
    text = forms.CharField(max_length=255,widget=forms.Textarea(attrs={'cols': 50, 'rows': 2}), label='')
    # author = forms.CharField(max_length=255,widget=forms.Textarea(attrs={'cols': 10, 'rows': 1}), label='')
    class Meta:
        model = Comment
        fields = ( 'text',)
from django import forms
from .models import Comment, Post

from django.contrib.auth.models import User

class NewComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(NewComment, self).__init__(*args, **kwargs)



class PostCreateForm(forms.ModelForm):
    title = forms.CharField(label='عنوان التدوينة')
    content = forms.CharField(label='نص التدوينة', widget=forms.Textarea)
    

    class Meta:
        model = Post
        fields = ['title', 'content'] 
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
           
        }

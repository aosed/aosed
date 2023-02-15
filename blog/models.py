from django.apps import AppConfig
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.contrib import messages

class Post(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    post_date = models.DateTimeField(default=timezone.now)
    post_update = models.DateTimeField(auto_now=True)
    likes = models.IntegerField(default=0)
    
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        # return '/detail/{}'.format(self.pk)
        return reverse('detail', args=[self.pk])

    class Meta:
        ordering = ('-post_date', )

class Notification(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    



class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name='الاسم')
    email = models.EmailField(verbose_name='البريد الإلكتروني')
    body = models.CharField( max_length=500 , verbose_name='تعليق جديد')
    comment_date = models.DateTimeField(auto_now_add=True)
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return 'علق {} على {}.'.format(self.name, self.post)

    class Meta:
        ordering = ('-comment_date',)
class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'

class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
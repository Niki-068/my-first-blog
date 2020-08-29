from django.conf import settings
from django.db import models
from django.utils import timezone
from accounts.models import Profile
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
    
    def approved_comments(self):
        return self.comments.filter(approved_comment=True)
    
    def increase_likes(self):
        self.likes = self.likes + 1

class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    #author = models.TextField(null=True,blank=True,)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='my_all_comments')
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)
    parent = models.ForeignKey('self', null=True,blank=True, on_delete=models.CASCADE, related_name='replies')

    class Meta:
        ordering = ('created_date',)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

    def children(self):
        return Comment.objects.filter(parent=self)

    def is_parent(self):
        if self.parent is not None:
            return False
        return True


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='my_Likes')
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE,related_name='all_Likes')
    created = models.DateTimeField(auto_now_add=True)

    

# @receiver(post_save, sender=User)
# def update_comment_signal(sender, instance, created, **kwargs):
#     comment = Comment.objects.get_or_create(user=instance)
#     instance.comment.save()

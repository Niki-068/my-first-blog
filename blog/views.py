from django.shortcuts import render
from django.utils import timezone
from .models import Post,Comment,Like
from django.shortcuts import render,redirect, get_object_or_404
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from .forms import PostForm, CommentForm
from rest_framework import generics
from .serializers import PostSerializer
from  mysite import helpers


class PostList(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

@login_required
def post_list(request):
    post_list = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    posts = helpers.pg_records(request, post_list, 5)
    return render(request, 'blog/post_list.html', {'posts': posts})

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post': post, 'form': form})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            #post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request,'blog/post_draft_list.html',{'posts':posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def publish(self):
    self.published_date = timezone.now()
    self.save()

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.filter(parent__isnull=True)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            parent_obj = None
            try:
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None
            if parent_id:
                parent_obj = Comment.objects.get(id=parent_id)
                if parent_obj:
                    reply_comment = form.save(commit=False)
                    reply_comment.parent = parent_obj
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def add_Likes(request, pk):
    new_like, created = Like.objects.get_or_create(user=request.user, post_id=pk)
    return redirect('post_detail', pk=new_like.post.pk)

def post_liked(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user_likes_this = post.all_Likes.filter(user=request.user) and True or False
    return redirect('post_detail', pk=post.pk)

# @login_required
# def add_Likes(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     # post.likes = post.likes + 1
#     # post.save()
#     return redirect('post_detail', pk=post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)



@login_required
def get_user_Posts(request):
    post_list = Post.objects.filter(author=request.user).order_by('created_date')
    posts = helpers.pg_records(request, post_list, 5)
    return render(request, 'blog/post_list.html', {'posts': posts})
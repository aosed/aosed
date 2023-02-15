from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect


from django.contrib.auth.models import User
from .models import Post, Comment ,Like ,Notification
from .forms import NewComment, PostCreateForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
def search(request):
    if request.method == 'POST':
        search_query = request.POST.get('User')
        if search_query:
            search_query = request.POST['search_query']
            # كود البحث الخاص بك
            search_results = User.objects.filter(username__icontains=search_query)
            # نتائج البحث الخاصة بك
            context = {'results':  search_results }
            return render(request, 'search_results.html', context)
        else:
            # قيمة البحث فارغة، يمكنك إعطاء رسالة خطأ للمستخدم
            return HttpResponse("Enter a valid search query.")
    else:
        # يمكنك إعطاء رسالة خطأ للمستخدم
        return HttpResponse("Invalid request method.")

def home(request):
    if request.method == 'POST':
        search_query = request.POST['search_query']
        search_results = User.objects.filter(username__icontains=search_query)
        return render(request, 'home.html', {'search_results': search_results})
    else:
        return render(request, 'blog/index.html')

def home(request ):
    posts = Post.objects.all() 
    paginator = Paginator(posts, 5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_page)
    context = {
        'title': 'الصفحة الرئيسية',
        'posts': posts,
        'page': page,
    }
    return render(request, 'blog/index.html', context)


def about(request):
    return render(request, 'blog/about.html', {'title': 'من أنا'})

def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = post.comments.all()

    # check before save data from comment form
    if request.method == 'POST':
        if request.user.is_authenticated:
            comment_form = NewComment(data=request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.post = post
                new_comment.name = request.user.username
                new_comment.email = request.user.email
                new_comment.save()
                # Deprecated line to prevent form to post data when refresh a page
                comment_form = NewComment()
                return redirect('detail', post_id)
        else:
            return redirect('login')
    else:
        comment_form = NewComment()

    context = {
        'title': post,
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    }

    return render(request, 'blog/detail.html' ,context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    # fields = ['title', 'content']
    template_name = 'blog/new_post.html'
    form_class = PostCreateForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'blog/post_update.html'
    form_class = PostCreateForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False


class PostDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
# views.py
# views.py
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    is_liked = False
    if request.user.is_authenticated:
        if Like.objects.filter(post=post, user=request.user).exists():
            Like.objects.filter(post=post, user=request.user).delete()
            is_liked = False
        else:
            Like.objects.create(post=post, user=request.user)
            is_liked = True
    context = {
        'post': post,
        'is_liked': is_liked,
        'total_likes': post.like_set.count(),
    }
    return JsonResponse(context)




def notification_view(request):
    notifications = Notification.objects.all().order_by('-timestamp')[:10]

    if request.user.is_authenticated:
        notifications = Notification.objects.all()
        return render(request, 'bese.html', {'notifications': notifications})
    else:
        return redirect('login')



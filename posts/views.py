from django.views import View
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model

from .models import Post
from .forms import PostForm, SearchForm
from comments.forms import CommentForm
from .utils import ObjectCreateMixin, ObjectUpdateMixin, ObjectDeleteMixin

User = get_user_model()


def posts_list_view(request):

    if not request.user.is_authenticated:
        return redirect(reverse('login_url'))

    if request.method == 'GET':
        if request.user.role == User.UserType.ORDINARY:
            posts = request.user.posts.all()
        else:
            posts = Post.objects.all()

        page_number = request.GET.get('page', 1)
        paginator = Paginator(posts, 3)
        page = paginator.get_page(page_number)

        if page.has_next():
            next_url = f'?page={page.number + 1}'
        else:
            next_url = f'?page={page.number}'

        if page.has_previous():
            previous_url = f'?page={page.number - 1}'
        else:
            previous_url = f'?page={page.number}'

        context = {'page': page,
                   'next_url': next_url,
                   'previous_url': previous_url}

        return render(request, 'posts/index.html', context=context)




    elif request.method == 'POST':
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            search_param = search_form.cleaned_data.get('search_param')
            filtered_posts = Post.objects.filter(title__icontains=search_param)
            return render(request, 'posts/index.html', context={'posts': filtered_posts})


def post_detail_view(request, id):
    post = get_object_or_404(Post, id=id)
    comments = post.comments.filter(active=True)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return render(request, 'posts/post_detail.html',
                          {'post': post,
                           'comments': comments,
                           'comment_form': comment_form,
                           'new_comment': new_comment})
    else:
        comment_form = CommentForm()
        return render(request, 'posts/post_detail.html',
                      {'post': post,
                       'comments': comments,
                       'comment_form': comment_form},
                      )


class PostCreateView(View, ObjectCreateMixin):
    form = PostForm
    template = 'posts/post_create.html'
    has_author = True


class PostUpdateView(View, ObjectUpdateMixin):
    bound_form = PostForm
    template = 'posts/post_update.html'
    obj_class = Post


class PostDeleteView(View, ObjectDeleteMixin):
    template = 'posts/post_delete.html'
    obj_class = Post
    redirect_template = 'posts_list_url'

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.generic import DeleteView, UpdateView
from django.db.models import Q
from .forms import CommentForm, LoginForm, RegistrationForm, PostForm
from .models import Category, HeroImage, FAQ, Post, Comment, PostViews, PostGallery, Like, Dislike
from django.core.paginator import Paginator


# CTRL + ALT + O
# Create your views here.


# Model.objects.get(поле_в_бд=значение)
# менеджер объектов (select (where), insert, update, delete)

# templatetags
def home_page(request):
    # hostname = socket.gethostname()
    # ip_address = socket.gethostbyname(hostname)
    # print(ip_address)
    # ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
    # print(ip)
    # получаем данные из таблицы
    # categories = Category.objects.all()  # QuerySet([Category(1), Category(2)])

    hero_images = HeroImage.objects.all()
    faqs = FAQ.objects.all()
    posts = Post.objects.all()

    page = request.GET.get('page')
    paginator = Paginator(posts, 4)
    # [1,2,3,4,5,6,7,8]
    # [(1,2,3,4), (5,6,7,8)]
    posts = paginator.get_page(page)

    # словарь в котором отдаем полученные данные из БД
    context = {
        # 'categories': categories
        'hero_images': hero_images,
        'faqs': faqs,
        'posts': posts,
    }
    return render(request, 'blog/index.html', context)


def contacts_page(request):
    return render(request, 'blog/contacts.html')


# category_pk
def category_posts(request, pk):
    category = Category.objects.get(pk=pk)
    # .get() - может отдать только 1 значение
    # если после фильтрации не получаем данные, будет ошибка

    # №1
    posts = Post.objects.filter(category=category)
    context = {
        'category': category,
        'posts': posts,
    }
    return render(request, 'blog/category.html', context)


# categories/<int:pk>/
# posts/<int:post_id>/
def post_detail(request, post_id):
    post = Post.objects.get(pk=post_id)
    gallery = post.gallery.all()

    all_posts = Post.objects.all()
    comments = Comment.objects.filter(post=post)

    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            # form.save()  # сохраняет сразу в БД
            form = form.save(commit=False)  # commit=False - не сохраняет в БД
            form.user = request.user
            form.post = post
            form.save()
            return redirect('post_detail', post_id=post_id)
    else:
        form = CommentForm()

    if not request.session.session_key:
        request.session.save()

    session_id = request.session.session_key
    post_view = PostViews.objects.filter(post=post, session_id=session_id).count()
    if post_view == 0 and session_id != 'None':
        post_view_obj = PostViews(post=post, session_id=session_id)
        post_view_obj.save()

        post.views += 1
        post.save()

        try:
            post.likes
        except Exception as e:
            Like.objects.create(post=post)

        try:
            post.dislikes
        except Exception as e:
            Dislike.objects.create(post=post)

    total_likes = post.likes.user.all().count()
    total_dislikes = post.dislikes.user.all().count()

    context = {
        'post': post,
        'all_posts': all_posts,
        'gallery': gallery,
        'form': form,
        'comments': comments,
        'total_likes': total_likes,
        'total_dislikes': total_dislikes,
    }
    return render(request, 'blog/post.html', context)


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    context = {
        'form': form,
    }
    return render(request, 'blog/login.html', context)


def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = RegistrationForm()

    context = {
        'form': form,
    }
    return render(request, 'blog/registration.html', context)


def user_logout(request):
    logout(request)
    return redirect('home')


def create_post_view(request):
    if request.method == 'POST':
        # print(request.POST)
        print(request.FILES)
        form = PostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            # form = Post
            form = form.save(commit=False)
            form.author = request.user
            form.save()

            for item in request.FILES.getlist('gallery'):
                new_photo = PostGallery(
                    post=form,
                    image=item
                )
                new_photo.save()

            return redirect('post_detail', post_id=form.pk)
    else:
        form = PostForm()

    context = {
        'form': form,
    }
    return render(request, 'blog/article_form.html', context)


class PostDeleteView(DeleteView):
    template_name = 'blog/post_confirm_delete.html'
    success_url = '/'
    model = Post
    pk_url_kwarg = 'post_id'


class UpdatePostView(UpdateView):
    form_class = PostForm
    model = Post
    pk_url_kwarg = 'post_id'
    success_url = '/'
    template_name = 'blog/article_form.html'


def search(request):
    # ?search=asdf
    # as
    query = request.GET.get('q')
    posts = Post.objects.filter(name__iregex=query)

    page = request.GET.get('page')
    paginator = Paginator(posts, 4)
    posts = paginator.get_page(page)
    context = {
        'posts': posts,
        'query': query
    }
    return render(request, 'blog/search_results.html', context)


def add_vote(request, post_id, action):
    post = Post.objects.get(pk=post_id)

    try:
        post.likes
    except Exception as e:
        Like.objects.create(post=post)

    try:
        post.dislikes
    except Exception as e:
        Dislike.objects.create(post=post)

    if action == 'add_like':
        if request.user in post.likes.user.all():
            post.likes.user.remove(request.user.pk)
        else:
            post.likes.user.add(request.user.pk)
            post.dislikes.user.remove(request.user.pk)

    elif action == 'add_dislike':
        if request.user in post.dislikes.user.all():
            post.dislikes.user.remove(request.user.pk)
        else:
            post.dislikes.user.add(request.user.pk)
            post.likes.user.remove(request.user.pk)

    return redirect('post_detail', post_id=post_id)








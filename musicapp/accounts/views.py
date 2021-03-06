from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from accounts.forms import EditProfileForm, ImageUploadForm, CreatePostForm, CreateCommentForm
from accounts.models import UserProfile, Posts, Comments
import datetime

# Create your views here.
def home(request):
    search_term = ''
    if 'search' in request.GET:
        search_term = request.GET['search']
        posts = Posts.objects.filter(title__icontains=search_term)
        posts = posts | Posts.objects.filter(artist__icontains=search_term)
        posts = posts | Posts.objects.filter(post__icontains=search_term)
        posts = posts | Posts.objects.filter(song__icontains=search_term)
    else:
        posts = Posts.objects.all().order_by("-id")
    posts = posts[:20]
    args = {'posts': posts, 'search_term': search_term}
    return render(request, 'accounts/home.html', args)

def popular(request):
    search_term = ''
    if 'search' in request.GET:
        search_term = request.GET['search']
        posts = Posts.objects.filter(title__icontains=search_term).order_by('-views')
        posts = posts | Posts.objects.filter(artist__icontains=search_term).order_by('-views')
        posts = posts | Posts.objects.filter(post__icontains=search_term).order_by('-views')
        posts = posts | Posts.objects.filter(song__icontains=search_term).order_by('-views')
    else:
        posts = Posts.objects.all().order_by('-views')
    posts = posts[:10]
    args = {'posts': posts}
    return render(request, 'accounts/popular.html', args)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/account')
    else:
        form = UserCreationForm()
        args = {'form': form}
        return render(request, 'accounts/reg_form.html', args)

def view_profile(request):
    try:
        username = request.GET.get('p');
        user = get_object_or_404(User,username=username)
        editable = False
        if request.user.is_authenticated and request.user == user:
            editable=True
            args = {'user': user, 'editable':editable}
            return render(request, 'accounts/profile.html', args)
    except:
            return HttpResponse('There was an error loading the page')

def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES)
        if form.is_valid():
            print("Hello")
            try:
                users = UserProfile.objects.all()
                user = users.get(user=request.user)
                user.song = form.cleaned_data['song']
                user.description = form.cleaned_data['description']
                user.album = form.cleaned_data['album']
                user.artist = form.cleaned_data['artist']
                user.save()
                return redirect('/account/profile/?p='+request.user.username)
            except:
                return HttpResponse("Something went wrong")
    else:
        form = EditProfileForm()
        args = {'form': form}
        return render(request, 'accounts/edit_profile.html', args)
    return HttpResponse("Something went wrong")

def upload_pic(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            users = UserProfile.objects.all()
            user = users.get(user=request.user)
            user.image.delete()
            user.image = form.cleaned_data['image']
            user.save()
            return redirect('/account/profile/edit/')
    else:
        form = ImageUploadForm()
    return HttpResponse("Must upload an image")

def create_post(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            #try:
                obj = Posts.objects.create()
                obj.fromUser = request.user
                obj.post = form.cleaned_data['post']
                obj.title = form.cleaned_data['title']
                obj.album = form.cleaned_data['album']
                obj.song = form.cleaned_data['song']
                obj.artist = form.cleaned_data['artist']
                obj.save()
                posts = Posts.objects.all().order_by("-id")
                args = {'posts': posts}
                return render(request, 'accounts/home.html', args) #Need to edit later
            #except:
                #return HttpResponse('Something went wrong when creating a post.')
    else:
        form = CreatePostForm()
        args = {'form': form}
        return render(request, 'accounts/create_post.html', args)
    return HttpResponse('Something went wrong')

def view_post(request, pk):
    post = Posts.objects.get(pk=pk)
    post.views = post.views + 1
    post.save()
    comments = Comments.objects.filter(commentPk=pk)
    delete = 0
    if request.user == post.fromUser:
        delete = 1
    now = datetime.datetime.now()
    args = {'post': post, 'comments': comments, 'delete': delete, 'now': now}
    return render(request, 'accounts/view_post.html', args)

def create_comment(request, pk):
    if request.method == 'POST':
        form = CreateCommentForm(request.POST)
        if form.is_valid():
            obj = Comments.objects.create()
            obj.commentUser = request.user
            obj.comment = form.cleaned_data['comment']
            obj.commentPk = pk
            obj.save()
            post = Posts.objects.get(pk=pk)
            comments = Comments.objects.filter(commentPk=pk).order_by("-id")
            delete = 0
            if request.user == post.fromUser:
                delete = 1
            now = datetime.datetime.now()
            args = {'post': post, 'comments': comments, 'delete': delete, 'now': now}
            return render(request, 'accounts/view_post.html', args)
    else:
        form = CreateCommentForm()
        args = {'form': form}
        return render(request, 'accounts/create_comment.html', args)
    return HttpResponse('Something went wrong')

def my_posts(request):
    posts = Posts.objects.filter(fromUser=request.user).order_by("-id")
    args = {'posts': posts}
    return render(request, 'accounts/my_posts.html', args)

def remove_post(request, pk):
    post = Posts.objects.get(pk=pk)
    post.delete()
    posts = Posts.objects.all().order_by("-id")
    args = {'posts': posts}
    return render(request, 'accounts/home.html', args)

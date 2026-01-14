from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView, DetailView,
    CreateView, UpdateView,
    DeleteView
)

from .models import post   # If your model is named post

# HOME PAGE (FUNCTION VIEW – OPTIONAL)
def home(request):
    context = {
        'posts': post.objects.all()
    }
    return render(request, 'blog/home.html', context)



# ALL POSTS
class PostListView(ListView):
    model = post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


# POSTS BY A PARTICULAR USER
class UserPostListView(ListView):
    model = post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return post.objects.filter(author=user).order_by('-date_posted')


# SINGLE POST
class PostDetailView(DetailView):
    model = post


# CREATE POST
class PostCreateView(LoginRequiredMixin, CreateView):
    model = post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# UPDATE POST
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post_obj = self.get_object()
        return self.request.user == post_obj.author


# DELETE POST
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = post
    success_url = '/'

    def test_func(self):
        post_obj = self.get_object()
        return self.request.user == post_obj.author


# ABOUT PAGE
def about(request):
    return render(request, 'blog/about.html', {'title': 'About', 'hide_sidebar': True})


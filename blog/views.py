from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import Post

from django.contrib.auth.models import User
# importing inbuilt views for class based view
from django.views.generic import ListView, DetailView,CreateView, UpdateView , DeleteView

# importing classes to add login functionality
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin


# Create your views here.

def home(request):
    context ={
        'posts':Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'     # <app>/<model>_<viewtype> but instead added template name
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 7


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'     # <app>/<model>_<viewtype> but instead added template name
    context_object_name = 'posts'
    paginate_by = 7

    def get_queryset(self):
        user = get_object_or_404(User, username = self.kwargs.get('username'))
        return Post.objects.filter(author= user).order_by('-date_posted')
        

class PostDetailView(DetailView):
    model = Post
     # template format django expects <app>/<model>_<viewtype> 


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title','contents']
    template_name = 'blog/add_post.html'
 
    def form_valid(self, form):
        form.instance.author = self.request.user   #set the author of form creating to the current logged in user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title','contents']
   
    def form_valid(self, form):
        form.instance.author = self.request.user   #set the author of form creating to the current logged in user
        return super().form_valid(form)

    def test_func(self):   # to test updating user is author
        post = self.get_object()  # to get the instance of the current post updating
        if self.request.user == post.author:  
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    template_name = 'blog/confirm.html'
    def test_func(self):      # to test deleting user is author
        post = self.get_object()  # to get the instance of the current post updating
        if self.request.user == post.author:  
            return True
        return False


    


def about(request):
    context ={
        'posts':Post.objects.all()
    }
    return render(request, 'blog/about.html', context)
    
    
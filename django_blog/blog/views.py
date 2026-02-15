from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("login")
    else:
        form = CustomUserCreationForm()
    return render(request, "blog/register.html", {"form": form})

@login_required
def profile(request):
    return render(request, 'blog/profile.html')

class BlogListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    ordering = ['-published_date']

class BlogDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"

class BlogCreateView(LoginRequiredMixin,CreateView):
    model = Post
    template_name = "blog/post_form.html"
    fields = ["title", "content"]
    success_url = reverse_lazy("posts")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class BlogUpdateView(LoginRequiredMixin,UpdateView):
    model = Post
    template_name = "blog/post_form.html"
    fields = ["title", "content"]
    success_url = reverse_lazy("posts")
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class BlogDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("posts")

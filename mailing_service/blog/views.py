from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import BlogPost
from .forms import BlogPostForm

def blog_list(request):
    blog_posts = BlogPost.objects.all()
    return render(request, 'blog/blog_list.html', {'blog_posts': blog_posts})

def blog_detail_view(request, pk):
    blog_post = get_object_or_404(BlogPost, pk=pk)
    blog_post.views += 1
    blog_post.save()
    return render(request, 'blog/blog_detail.html', {'blog_post': blog_post})

class BlogPostCreateView(LoginRequiredMixin, CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog/blog_form.html'
    success_url = reverse_lazy('blog_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class BlogPostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog/blog_form.html'
    success_url = reverse_lazy('blog_list')

    def test_func(self):
        blog_post = self.get_object()
        return self.request.user == blog_post.author

class BlogPostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = BlogPost
    template_name = 'blog/blog_confirm_delete.html'
    success_url = reverse_lazy('blog_list')

    def test_func(self):
        blog_post = self.get_object()
        return self.request.user == blog_post.author

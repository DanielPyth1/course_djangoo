from django.shortcuts import render, get_object_or_404
from .models import BlogPost

def blog_list(request):
    # Получаем все записи блога из базы данных
    blog_posts = BlogPost.objects.all()
    return render(request, 'blog/blog_list.html', {'blog_posts': blog_posts})


def blog_detail_view(request, pk):
    # Получаем объект статьи блога
    blog_post = get_object_or_404(BlogPost, pk=pk)

    # Увеличиваем счетчик просмотров
    blog_post.views += 1
    blog_post.save()

    # Передаем объект в шаблон
    return render(request, 'blog/blog_detail.html', {'blog_post': blog_post})
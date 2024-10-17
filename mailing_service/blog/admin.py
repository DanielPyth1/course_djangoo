from django.contrib import admin
from .models import BlogPost

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'views')
    search_fields = ('title', 'content')

admin.site.register(BlogPost, BlogPostAdmin)
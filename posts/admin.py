from django.contrib import admin
from .models import User, Post, Comment

admin.site.register(User)
admin.site.register(Comment)



@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at']
    list_filter = ['created_at']
    search_fields = ['title', 'author__username']
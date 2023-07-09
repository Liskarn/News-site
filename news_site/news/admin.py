from django.contrib import admin
from .models import Post, Comment
from .models import Vote


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'link', 'description', 'pub_date', 'author']
    search_fields = ['title', 'description']
    list_filter = ['pub_date', 'author']

admin.site.register(Post, PostAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'text', 'created_date']
    search_fields = ['text']
    list_filter = ['created_date', 'author']

admin.site.register(Comment, CommentAdmin)

class VoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'value']
    list_filter = ['value']

admin.site.register(Vote, VoteAdmin)
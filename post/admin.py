from django.contrib import admin
from post.models import Post, Comment

class CommentAdmin(admin.ModelAdmin):
	list_display = ('post', 'commenter', 'comment', 'date_commented')

class PostAdmin(admin.ModelAdmin):
	list_display = ('caption', 'author', 'date_published')

admin.site.register(Post, PostAdmin)

admin.site.register(Comment, CommentAdmin)
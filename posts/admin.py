from django.contrib import admin
from .models import (Post, Category, Comment, Like)
from django_summernote.admin import SummernoteModelAdmin


class Categorias(admin.ModelAdmin):
    search_fields = ['id','name']
    list_display = ['id', 'name','updated_at']
    
    class Meta:
        model = Category


def No_visible(modeladmin, request, queryset):
    for post in queryset:
        post.status = False
        post.save()
No_visible.short_description = 'Ocultar Post'

def visible(modeladmin, request, queryset):
    for post in queryset:
        post.status = True
        post.save()
visible.short_description = 'Mostrar Post'


class post(SummernoteModelAdmin):
    filter_fields = ['status']
    list_display = ['id','title','description','post_start_date','post_end_date','tags','status','created_at','updated_at']

    actions = [No_visible, visible, ]

    def get_ordering(self, request):
        return ['-created_at'] 
    
    class Meta:
        model = Post


class Comments(SummernoteModelAdmin):
    list_display = ['id','author','post','comment','created_at','updated_at']

    def get_ordering(self, request):
        return ['-created_at'] 
    
    class Meta:
        model = Comment


class Likes(SummernoteModelAdmin):
    list_display = ['id','user','post','created_at','updated_at']

    def get_ordering(self, request):
        return ['-created_at'] 
    
    class Meta:
        model = Like


admin.site.register(Post,post)
admin.site.register(Category,Categorias)
admin.site.register(Comment,Comments)
admin.site.register(Like,Likes)

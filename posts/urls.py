from django.urls import path

from .views import (SelfPostView, DetailPost, PostNew, PostEdit, PostDelete,\
    CategoryView, CategoryNew, CategoryEdit, CategoryDelete, \
       CommentDelete, PostLikeAction)

urlpatterns = [
    # post urls
    path('post/self', SelfPostView.as_view(), name = 'self_list_post'),
    path('post/new', PostNew.as_view(), name = 'new_post'),
    path('post/edit/<int:pk>', PostEdit.as_view(), name = 'post_edit'),
    path('post/detail/<slug:slug>', DetailPost.as_view(), name = 'detail_post'),
    path('post/delete/<int:pk>', PostDelete.as_view(), name = 'delete_post'),

    # category urls
    path('category/', CategoryView.as_view(), name = 'list_category'),
    path('categoty/new', CategoryNew.as_view(), name = 'new_category'),
    path('category/edit/<int:pk>', CategoryEdit.as_view(), name = 'edit_category'),
    path('category/delete/<int:pk>', CategoryDelete.as_view(), name = 'delete_category'),

    # comment urls
    path('comments/delete/<int:pk>', CommentDelete.as_view(), name = 'delete_comment'),

    #like action
    path('post/like/action/<int:id_post>', PostLikeAction, name = 'post_like_action'),
]
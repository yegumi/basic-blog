from django.urls import path
from . import views
app_name='home'
urlpatterns=[
    path('',views.HomeView.as_view(), name='home'),
    path('search/',views.SearchView.as_view(),name='search_results'),
    path('detail/ <int:post_id>/ <slug:post_slug>',views.PostCommentView.as_view(),name='detail'),
    path('detail/delete/<int:post_id>/',views.PostDeleteView.as_view(),name='delete_post'),
    path('detail/update/<int:post_id>/',views.PostUpdateView.as_view(),name='update_post'),
    path('detail/create/',views.PostCreateView.as_view(),name='create_post'),
    path('reply/<int:post_id>/<comment_id>',views.CommentReplyView.as_view(),name='reply_comment'),
    path('like/<int:user_id>/<post_id>',views.LikeView.as_view(),name='like')


]
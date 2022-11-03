from django.urls import path
from . import views

urlpatterns = [
    path('<int:song_id>/', views.SongView.as_view(), name='song_view'),    
    path('<int:song_id>/song_like/', views.SongLikeView.as_view(), name='song_like_view'),
    path('<int:song_id>/comment/', views.CommentView.as_view(), name='comment_view'),
    path('<int:song_id>/comment/<int:comment_id>/', views.CommentDetailView.as_view(), name='comment_detail_view'),
]
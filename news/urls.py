from .views import *
from django.urls import path, include


urlpatterns = [
    path('home/', HomeArticleListView.as_view()),
    path('<str:category>/', ArticleListCreateAPIView.as_view()),
    path('<str:category>/<int:pk>/', ArticleDetailAPIView.as_view()),
    path('<int:pk>/<str:action_type>', ArticleActionView.as_view()),
    path('<int:article_id>/comments/', CommentListCreateAPIView.as_view())
]

from .views import *
from rest_framework.routers import DefaultRouter
from django.urls import path, include


router = DefaultRouter()


all_article_list = AllArticleViewSet.as_view({
    'get': 'list',
    'post': 'create'
})


comment_list = CommentViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

urlpatterns = [
    path('', include(router.urls)),
    path('home/', all_article_list),
    path('<int:article_id>/comments/', comment_list, name='comment-list'),
    path('<str:category>/', ArticleListCreateAPIView.as_view()),
    path('<str:category>/<int:pk>/', ArticleDetailAPIView.as_view()),
    # path('<int:pk>/<str:action_type>', ArticleActionView.as_view())
]

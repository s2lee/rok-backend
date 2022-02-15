from .views import *
from rest_framework.routers import DefaultRouter
from django.urls import path, include


router = DefaultRouter()

article_list = ArticleViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

all_article_list = AllArticleViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

article_detail = ArticleViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

comment_list = CommentViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

urlpatterns = [
    path('', include(router.urls)),
    path('home/', all_article_list),
    path('<str:category>/', article_list, name='article-list'),
    path('<str:category>/<int:pk>/', article_detail, name='article-detail'),
    path('<int:article_id>/comments/', comment_list, name='comment-list'),
    path('<int:pk>/<str:action_type>', action_button, name='action-button'),
    path('test/<str:category>/', ArticleSectionListAPIView.as_view(), )
]

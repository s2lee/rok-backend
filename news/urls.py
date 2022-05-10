from django.urls import path, re_path

from .views import (ArticleDetailAPIView, ArticleListCreateAPIView,
                    ArticleVoteView, CommentListCreateAPIView, HomeArticleView,
                    SearchNewsByDate)


urlpatterns = [
    path("home/", HomeArticleView.as_view()),
    path("<str:category>/", ArticleListCreateAPIView.as_view()),
    path("<str:category>/<int:pk>/", ArticleDetailAPIView.as_view()),
    path("<int:article_id>/vote/<str:choice>/", ArticleVoteView.as_view()),
    path("<int:article_id>/comments/", CommentListCreateAPIView.as_view()),
    re_path(
        r"^newspaper/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/",
        SearchNewsByDate.as_view(),
    ),
]

from datetime import datetime, date

from django.shortcuts import get_object_or_404
from django.db.models import Count

from rest_framework import status
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import HomeArticleSerializer, ArticleSectionSerializer, ArticleCreateSerializer,\
    ArticleDetailSerializer, CommentSerializer, SearchNewsByDateSerializer, HomeTopArticleSerializer
from .models import Article, Comment, Category


class HomeArticleListView(ListAPIView):
    serializer_class = HomeArticleSerializer
    permission_classes = (AllowAny, )
    today = date.today()

    def list(self, request, *args, **kwargs):
        response = Response(self.get_most_voted_articles(), status=status.HTTP_200_OK)
        response.data['article'] = self.get_latest_articles()
        return response

    def get_latest_articles(self):
        articles = Article.objects.select_related(
            'author', 'category').filter(date_posted__date=self.today)[:10]
        article_serializer = self.get_serializer(articles, many=True)
        return article_serializer.data

    def get_most_voted_articles(self):
        temp = {}
        categories = Category.objects.all()
        for category in categories:
            top_articles = Article.objects_sorted_by_vote.select_related(
                'category').filter(date_posted__date=self.today, category__name=category)[:3]
            top_article_serializer = HomeTopArticleSerializer(top_articles, many=True)
            temp[f'{category}'] = top_article_serializer.data
        return temp


class ArticleListCreateAPIView(ListCreateAPIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = (AllowAny,)
        else:
            self.permission_classes = (IsAuthenticated, )

        return super(ArticleListCreateAPIView, self).get_permissions()

    def get_queryset(self):
        return Article.objects.select_related('author').prefetch_related(
            'spear', 'shield', 'comment').filter(category__name=self.kwargs.get('category'))

    def list(self, request, *args, **kwargs):
        articles = self.get_queryset()
        top_articles = articles.annotate(total_votes=Count(
            'spear', distinct=True) - Count('shield', distinct=True)).order_by('-total_votes')[:3]
        article_serializer = self.get_serializer(articles, many=True)
        top_article_serializer = self.get_serializer(top_articles, many=True)
        return Response({
            'articles': article_serializer.data,
            'top_articles': top_article_serializer.data,
        })

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ArticleSectionSerializer
        else:
            return ArticleCreateSerializer

    def perform_create(self, serializer):
        category = Category.objects.get(name=self.kwargs.get('category'))
        serializer.save(author=self.request.user, category=category)


class ArticleDetailAPIView(RetrieveAPIView):
    serializer_class = ArticleDetailSerializer
    permission_classes = (AllowAny, )
    queryset = Article.objects.select_related('author').prefetch_related(
            'spear', 'shield').all()


class ArticleVoteView(GenericAPIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        return self.vote_for_article()

    def get_object(self):
        article_id = self.kwargs.get('article_id')
        return get_object_or_404(Article, pk=article_id)

    def get_choice(self):
        article = self.get_object()
        choice = self.kwargs.get('choice')
        return getattr(article, choice)

    def vote_for_article(self):
        voted_article = self.get_choice()
        user = self.request.user
        response = Response({'detail': '성공적으로 사용.'}, status=status.HTTP_200_OK)
        if voted_article.filter(id=user.id).exists():
            voted_article.remove(user)
            response.data = {'detail': '사용을 취소합니다.'}
        else:
            voted_article.add(user)

        response.data['total_choice_count'] = voted_article.count()
        return response


class CommentListCreateAPIView(ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = (AllowAny, )
        else:
            self.permission_classes = (IsAuthenticated, )

        return super(CommentListCreateAPIView, self).get_permissions()

    def get_queryset(self):
        article_id = self.kwargs.get('article_id')
        return Comment.objects.select_related('author').prefetch_related(
            'reply__author').filter(parent=None, article=article_id)

    def perform_create(self, serializer):
        parent = self.request.data['parent']
        comment_qs = None
        if parent:
            comment_qs = Comment.objects.get(id=parent)

        serializer.save(author=self.request.user, parent=comment_qs)


class SearchNewsByDate(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SearchNewsByDateSerializer

    def get(self, request, *args, **kwargs):
        return self.get_response()

    def get_news_date(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        return datetime.strptime(f'{year}-{month}-{day}', "%Y-%m-%d")

    def get_queryset(self):
        news_date = self.get_news_date()
        articles = Article.objects_sorted_by_vote.select_related(
            'category').prefetch_related('comment').filter(
            date_posted__date=news_date, is_news=True)
        return articles

    def divide_articles_by_category(self):
        articles = self.get_queryset()
        categories = Category.objects.all()
        divided_articles = {}
        for category in categories:
            article_by_category = articles.filter(category__name=category)[:3]
            serializer = self.get_serializer(article_by_category, many=True)
            divided_articles[f'{category}'] = serializer.data
        return divided_articles

    def get_response(self):
        divided_articles = self.divide_articles_by_category()
        response = Response(divided_articles, status=status.HTTP_200_OK)
        if not any(divided_articles.values()):
            response.data = {'detail': f'{self.get_news_date()}의 기사는 없습니다.'}
        return response

from django.shortcuts import get_object_or_404
from django.db.models import Count

from rest_framework import viewsets, status
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import *
from .models import Article, Comment, Category


class AllArticleViewSet(viewsets.ModelViewSet):
    serializer_class = AllArticleSerializer
    queryset = Article.objects.all()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(parent=None,
                                      article=self.kwargs.get('article_id'))

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ArticleListCreateAPIView(ListCreateAPIView):
    def get_queryset(self):
        return Article.objects.filter(category__name=self.kwargs.get('category'))

    def list(self, request, *args, **kwargs):
        article = self.get_queryset()
        top_article = article.annotate(
            total_point=Count('spear') - Count('shield')).order_by('-total_point')[:3]
        article_serializer = self.get_serializer(article, many=True)
        top_article_serializer = self.get_serializer(top_article, many=True)
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
    queryset = Article.objects.select_related('author').prefetch_related(
            'spear', 'shield').all()


class ArticleActionView(GenericAPIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, pk, action_type):
        article = get_object_or_404(Article, pk=pk)
        article_action = getattr(article, action_type)
        user = request.user
        response = Response(
            {'detail': f'{action_type} 성공적으로 사용.'},
            status=status.HTTP_200_OK,
        )
        if article.author != user:
            if article_action.filter(id=user.id).exists():
                article_action.remove(user)
                response.data = {'detail': f'{action_type} 사용을 취소합니다.'}
            else:
                article_action.add(user)
        else:
            response.data = {'detail': '기사 작성자는 사용할 수 없습니다.'}
            response.status_code = status.HTTP_401_UNAUTHORIZED
        response.data['total_action_count'] = article_action.count()
        return response


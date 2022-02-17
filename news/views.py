from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from .serializers import *
from .models import Article, Comment, Category


class AllArticleViewSet(viewsets.ModelViewSet):
    serializer_class = AllArticleSerializer
    queryset = Article.objects.all()


class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        return Article.objects.filter(category__name=self.kwargs.get('category'))

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(parent=None,
                                      article=self.kwargs.get('article_id'))

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def action_button(request, pk, action_type):
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


class ArticleSectionListAPIView(APIView):
    def get(self, request, category):
        article = Article.objects.filter(category__name=category)
        top_article = article.order_by('date_posted')[:2]

        article_serializer = ArticleSectionSerializer(article, many=True)
        top_article_serializer = TopArticleSerializer(top_article, many=True)

        return Response({
            'articles': article_serializer.data,
            'top_articles': top_article_serializer.data
        })

# class ArticleSectionListAPIView(generics.ListAPIView):
#     serializer_class = ArticleSectionSerializer
#
#     def get_queryset(self):
#         return Article.objects.filter(category__name=self.kwargs.get('category'))

# select, prefetch -> object가 아니라 queryset에 해야하고. Retrieve는 category 연결안해도 pk로 찾음
class ArticleDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ArticleDetailSerializer
    queryset = Article.objects.select_related('author').prefetch_related(
            'spear', 'shield').all()

    # def get_object(self):
    #     article = Article.objects.select_related('author').prefetch_related(
    #         'spear', 'shield')
    #     return article


class ArticleListCreateAPIView(generics.ListCreateAPIView):
    def get_queryset(self):
        return Article.objects.filter(category__name=self.kwargs.get('category'))

    # def list(self, request, *args, **kwargs):
    #     # response = super().list(request, *args, **kwargs)
    #     article = self.get_queryset()
    #     top_article = article.order_by('date_posted')[:2]
    #     top_article_serializer = TopArticleSerializer(top_article, many=True)
    #     serializer = self.get_serializer()
    #     # serializer.data.append(top_article_serializer)
    #     # response.data['top_articles'] = top_article_serializer.data
    #     return Response({
    #         'article': serializer.data,
    #         'top_article': top_article_serializer
    #     })

    def list(self, request, *args, **kwargs):
        article = self.get_queryset()
        top_article = article.order_by('date_posted')[:2]
        article_serializer = self.get_serializer(article, many=True)
        top_article_serializer = TopArticleSerializer(top_article, many=True)
        return Response({
            'articles': article_serializer.data,
            'top_articles': top_article_serializer.data
        })

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ArticleSectionSerializer
        else:
            return ArticleCreateSerializer

    def perform_create(self, serializer):
        category = Category.objects.get(name=self.kwargs.get('category'))
        serializer.save(author=self.request.user, category=category)


class ArticleViewSet2(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      GenericViewSet):

    serializer_class_by_action = {
        'list': ArticleSectionSerializer,
        'create': ArticleCreateSerializer,
        'retrieve': ArticleDetailSerializer,
    }

    def get_serializer_class(self):
        if hasattr(self, 'serializer_class_by_action'):
            return self.serializer_class_by_action.get(self.action, self.serializer_class)
        return super().get_serializer_class()

    def perform_create(self, serializer):
        category = Category.objects.get(name=self.kwargs.get('category'))
        serializer.save(author=self.request.user, category=category)

    def get_queryset(self):
        return Article.objects.filter(category__name=self.kwargs.get('category'))


from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .models import Article, Comment


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


# class ArticleSectionListAPIView(APIView):
#     def get(self, request):
#         article = Article.objects.filter(category__name=self.kwargs.get('category'))
#         top_article = article.order_by('date_posted')[:3]
#
#         article_serializer = ArticleSectionSerializer(article, many=True)
#         top_article_serializer = TopArticleSerializer(top_article, many=True)
#
#         return Response({
#             'articles': article_serializer.data,
#             'top_articles': top_article_serializer.data
#         })

class ArticleSectionListAPIView(generics.ListAPIView):
    serializer_class = ArticleSectionSerializer

    def get_queryset(self):
        return Article.objects.filter(category__name=self.kwargs.get('category'))


# category 넣기
class ArticleCreateAPIView(generics.CreateAPIView):
    serializer_class = ArticleCreateSerializer
    permission_classes = IsAuthenticated

    def perform_create(self, serializer):
        category = self.kwargs.get('category')
        serializer.save(author=self.request.user, category=category.id)


# select, prefetch
class ArticleRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = ArticleDetailSerializer

    def get_queryset(self):
        return Article.objects.filter(category__name=self.kwargs.get('category'))


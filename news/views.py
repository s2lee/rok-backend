from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import ArticleSerializer, AllArticleSerializer, CommentSerializer
from .models import Article, Comment


# from users.models import Item


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
        return Comment.objects.filter(parent=None, article=self.kwargs.get('article_id'))

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# class ItemApiView(APIView):
#     def post(self, request, pk, item_type):
#         user = request.user
#         article = get_object_or_404(Article, pk=pk)
#         item = Item.objects.get(user=user)
#         success = True

#         def use_item():
#             nonlocal success
#             _article = getattr(article, item_type)
#             _item = getattr(item, item_type)
#             if _article.filter(id=user.id).exists():
#                 _article.remove(user)
#             else:
#                 if _item >= 1:
#                     _article.add(user)
#                     _item -= 1
#                     setattr(item, item_type, _item)
#                     item.save()
#                 else:
#                     success = False

#         use_item()
#         message = f'{item_type} 성공적으로 사용' if success else f'{item_type} 부족'
#         return Response({"message": message})
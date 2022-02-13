from rest_framework import serializers
from .models import Article, Comment


class AllArticleSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Article
        fields = ('id', 'category_name', 'title', 'date_posted')


class ArticleSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    author_name = serializers.ReadOnlyField(source='author.username')
    total_spear = serializers.SerializerMethodField()
    total_shield = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ('id', 'category', 'title', 'contents', 'date_posted', 'spear', 'shield', 'category_name',
                  'author_name', 'image', 'total_spear', 'total_shield')

    def get_total_spear(self, obj):
        return obj.spear.count()

    def get_total_shield(self, obj):
        return obj.shield.count()


class CommentSerializer(serializers.ModelSerializer):
    reply = serializers.SerializerMethodField()
    author_name = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ('id', 'article', 'author_name', 'contents', 'date_created', 'reply')

    def get_reply(self, instance):
        serializer = self.__class__(instance.reply, many=True)
        serializer.bind('', self)
        return serializer.data

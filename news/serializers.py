from rest_framework import serializers
from .models import Article, Comment


class HomeArticleSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ('id', 'category_name', 'title', 'contents',
                  'image', 'date_posted', 'comments_count')

    def get_comments_count(self, obj):
        return obj.comment.count()


class ArticleSectionSerializer(serializers.ModelSerializer):
    nickname = serializers.ReadOnlyField(source='author.nickname')
    comments_count = serializers.SerializerMethodField()
    total_point = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ('id', 'title', 'contents', 'date_posted',
                  'nickname', 'image', 'comments_count', 'total_point')

    def get_comments_count(self, obj):
        return obj.comment.count()

    def get_total_point(self, obj):
        return obj.spear.count() - obj.shield.count()


class ArticleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('title', 'contents', 'image')


class ArticleDetailSerializer(serializers.ModelSerializer):
    nickname = serializers.ReadOnlyField(source='author.nickname')
    spear_count = serializers.SerializerMethodField()
    shield_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    date_posted = serializers.DateTimeField(format="%Y.%m.%d %H:%M")

    class Meta:
        model = Article
        fields = ('title', 'contents', 'nickname', 'date_posted', 'spear', 'shield',
                  'image', 'spear_count', 'shield_count', 'comments_count')

    def get_spear_count(self, obj):
        return obj.spear.count()

    def get_shield_count(self, obj):
        return obj.shield.count()

    def get_comments_count(self, obj):
        return obj.comment.count()


class CommentSerializer(serializers.ModelSerializer):
    reply = serializers.SerializerMethodField()
    nickname = serializers.ReadOnlyField(source='author.nickname')
    date_created = serializers.DateTimeField(format="%Y.%m.%d %H:%M", read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'article', 'nickname', 'contents', 'date_created', 'parent', 'reply')

    def get_reply(self, instance):
        serializer = self.__class__(instance.reply, many=True)
        serializer.bind('', self)
        return serializer.data

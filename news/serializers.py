from rest_framework import serializers
from .models import Article, Comment


class CommonFieldMixin(serializers.Serializer):
    nickname = serializers.ReadOnlyField(source='author.nickname')
    category_name = serializers.ReadOnlyField(source='category.name')
    comments_count = serializers.SerializerMethodField()

    def get_comments_count(self, obj):
        return obj.comment.count()


class HomeTopArticleSerializer(CommonFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'category_name', 'title', 'contents',
                  'image')


class HomeArticleSerializer(CommonFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'category_name', 'title', 'nickname')


class ArticleSectionSerializer(CommonFieldMixin, serializers.ModelSerializer):
    total_votes = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ('id', 'title', 'contents', 'date_posted',
                  'nickname', 'image', 'comments_count', 'total_votes')

    def get_total_votes(self, obj):
        return obj.spear.count() - obj.shield.count()


class ArticleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('title', 'contents', 'image')


class ArticleDetailSerializer(CommonFieldMixin, serializers.ModelSerializer):
    spear_count = serializers.SerializerMethodField()
    shield_count = serializers.SerializerMethodField()
    date_posted = serializers.DateTimeField(format="%Y.%m.%d %H:%M")

    class Meta:
        model = Article
        fields = ('id', 'title', 'contents', 'nickname', 'author',
                  'date_posted', 'spear', 'shield', 'image', 'spear_count',
                  'shield_count', 'comments_count')

    def get_spear_count(self, obj):
        return obj.spear.count()

    def get_shield_count(self, obj):
        return obj.shield.count()


class CommentSerializer(CommonFieldMixin, serializers.ModelSerializer):
    reply = serializers.SerializerMethodField()
    date_created = serializers.DateTimeField(format="%Y.%m.%d %H:%M", read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'article', 'nickname', 'contents', 'date_created', 'parent', 'reply')

    def get_reply(self, instance):
        serializer = self.__class__(instance.reply, many=True)
        serializer.bind('', self)
        return serializer.data


class SearchNewsByDateSerializer(CommonFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'category_name', 'title', 'contents', 'image', 'comments_count')

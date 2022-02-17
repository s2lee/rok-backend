from rest_framework import serializers
from .models import Article, Comment

# homeArticle id, category_na,e, title, 'date_posted' 필요
class AllArticleSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Article
        fields = ('id', 'category_name', 'title', 'date_posted')


class ArticleSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    author_name = serializers.ReadOnlyField(source='author.username')
    spear_count = serializers.SerializerMethodField()
    shield_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ('id', 'category', 'title', 'contents', 'date_posted', 'spear', 'shield', 'category_name',
                  'author_name', 'image', 'spear_count', 'shield_count', 'comments_count')

    def get_spear_count(self, obj):
        return obj.spear.count()

    def get_shield_count(self, obj):
        return obj.shield.count()

    def get_comments_count(self, obj):
        return obj.comment.count()


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


class TopArticleSerializer(serializers.ModelSerializer):
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ('id', 'title', 'contents', 'date_posted', 'image', 'comments_count')

    def get_comments_count(self, obj):
        return obj.comment.count()


class ArticleSectionSerializer(serializers.ModelSerializer):
    nickname = serializers.ReadOnlyField(source='author.nickname')
    comments_count = serializers.SerializerMethodField()
    # top_articles = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ('id', 'title', 'date_posted', 'nickname', 'image', 'comments_count')

    def get_comments_count(self, obj):
        return obj.comment.count()

    # def get_top_articles(self, obj):
    #     data = TopArticleSerializer(obj, many=True).data
    #     return data

    # def get_top_article(self, obj):
    #     article = obj.objects.all()
    #     return TopArticleSerializer(article, many=True)

class ArticleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('title', 'contents', 'image')


class ArticleDetailSerializer(serializers.ModelSerializer):
    nickname = serializers.ReadOnlyField(source='author.nickname')
    spear_count = serializers.SerializerMethodField()
    shield_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

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



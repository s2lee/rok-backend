from rest_framework import serializers

from .models import Article, Comment


class CommonFieldMixin(serializers.Serializer):
    nickname = serializers.ReadOnlyField(source="author.nickname")
    category_name = serializers.ReadOnlyField(source="category.name")


class HomeArticleSerializer(CommonFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ("id", "category_name", "title", "contents", "image")


class ArticleSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ("id", "title", "contents", "date_posted", "image")


class ArticleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ("title", "contents", "image")


class ArticleDetailSerializer(CommonFieldMixin, serializers.ModelSerializer):
    num_spear = serializers.IntegerField(source="get_total_spear")
    num_shield = serializers.IntegerField(source="get_total_shield")
    date_posted = serializers.DateTimeField(format="%Y.%m.%d %H:%M")

    class Meta:
        model = Article
        fields = (
            "id",
            "title",
            "contents",
            "nickname",
            "author",
            "date_posted",
            "spear",
            "shield",
            "image",
            "num_spear",
            "num_shield",
        )


class CommentSerializer(CommonFieldMixin, serializers.ModelSerializer):
    reply = serializers.SerializerMethodField()
    date_created = serializers.DateTimeField(format="%Y.%m.%d %H:%M", read_only=True)

    class Meta:
        model = Comment
        fields = (
            "id",
            "article",
            "nickname",
            "contents",
            "date_created",
            "parent",
            "reply",
        )

    def get_reply(self, instance):
        serializer = self.__class__(instance.reply, many=True)
        serializer.bind("", self)
        return serializer.data


class SearchNewsByDateSerializer(CommonFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ("id", "category_name", "title", "contents", "image")

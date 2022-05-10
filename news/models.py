from django.conf import settings
from django.db import models
from django.db.models import Count

User = settings.AUTH_USER_MODEL


class ArticleVoteManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(
                total_votes=Count("spear", distinct=True)
                - Count("shield", distinct=True)
            )
            .order_by("-total_votes")
        )


class Category(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=130)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="article"
    )
    contents = models.TextField(max_length=1000)
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    spear = models.ManyToManyField(User, blank=True, related_name="spear")
    shield = models.ManyToManyField(User, blank=True, related_name="shield")
    image = models.ImageField(blank=True, null=True, upload_to="article/%Y/%m/%d")
    is_news = models.BooleanField(default=False)

    def __str__(self):
        return str(self.title)[:10]

    def get_total_spear(self):
        return self.spear.count()

    def get_total_shield(self):
        return self.shield.count()

    class Meta:
        ordering = ["-date_posted"]

    objects = models.Manager()
    objects_sorted_by_vote = ArticleVoteManager()


class Comment(models.Model):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="comment"
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    contents = models.TextField(max_length=600)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="reply"
    )
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.contents)[:10]

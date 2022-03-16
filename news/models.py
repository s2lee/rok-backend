from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=30)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='article')
    contents = models.TextField(max_length=150)
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    spear = models.ManyToManyField(User, blank=True, related_name='spear')
    shield = models.ManyToManyField(User, blank=True, related_name='shield')
    image = models.ImageField(blank=True, null=True, upload_to="article/%Y/%m/%d")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-date_posted"]

    objects = models.Manager()


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comment')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    contents = models.TextField(max_length=600)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                               related_name='reply')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.contents

    objects = models.Manager()

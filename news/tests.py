from django.contrib.auth import get_user_model
from django.test import override_settings
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Article, Category, Comment
from .tasks import choose_article_every_midnight

User = get_user_model()


class NewsAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user", password="test_password", nickname="test_nickname"
        )
        self.category = Category.objects.create(name="art")
        self.article = Article.objects.create(
            title="Fractal is wonderful",
            category=self.category,
            contents="Fractal is ...",
            author=self.user,
            is_news=True,
        )
        self.article_count = Article.objects.all().count()
        self.comment = Comment.objects.create(
            article=self.article, author=self.user, contents="test comment"
        )
        self.current_date_time = timezone.now()

    def test_article_list(self):
        response = self.client.get("/news/art/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_article_create(self):
        data = {
            "title": "White",
            "category": self.category.id,
            "contents": "leverage",
            "author": self.user,
        }
        response = self.client.post("/news/art/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=self.user)
        response = self.client.post("/news/art/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Article.objects.all().count(), self.article_count + 1)

        new_article = Article.objects.latest("id")
        self.assertEqual(new_article.title, data["title"])

    def test_article_detail(self):
        response = self.client.get(f"/news/art/{self.article.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Fractal is wonderful")

    def test_article_vote(self):
        response = self.client.post(f"/news/{self.article.id}/vote/shield/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=self.user)
        response = self.client.post(f"/news/{self.article.id}/vote/spear/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["detail"], "성공적으로 사용.")
        self.assertEqual(
            response.data["total_choice_count"], self.article.spear.count()
        )
        self.assertEqual(self.article.spear.count(), 1)

        self.client.force_authenticate(user=self.user)
        response = self.client.post(f"/news/{self.article.id}/vote/spear/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["detail"], "사용을 취소합니다.")
        self.assertEqual(self.article.spear.count(), 0)

    def test_comment_list(self):
        response = self.client.get(f"/news/{self.article.id}/comments/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_comment_create(self):
        data = {
            "article": self.article.id,
            "contents": "How calculus makes the world smarter",
            "author": self.user,
            "parent": self.comment.id,
        }
        response = self.client.post(f"/news/{self.article.id}/comments/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=self.user)
        response = self.client.post(f"/news/{self.article.id}/comments/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_search_news_by_date(self):
        news_date = self.current_date_time.strftime("%Y/%m/%d")
        response = self.client.get(f"/news/newspaper/{news_date}/")
        self.assertIn("art", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get("/news/newspaper/2022/04/06/")
        self.assertEqual(response.data["detail"], "2022-04-06 00:00:00의 기사는 없습니다.")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @override_settings(CELERY_ALWAYS_EAGER=True)
    def test_choose_article_every_midnight(self):
        self.assertEqual(choose_article_every_midnight(), "success")

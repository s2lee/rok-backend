from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Article, Category, Comment


User = get_user_model()


class NewsAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='username',
                                             password='password123',
                                             nickname='test_nickname')
        self.category = Category.objects.create(name='art')
        self.article = Article.objects.create(title='Fractal is wonderful',
                                              category=self.category,
                                              contents='Fractal is ...',
                                              author=self.user)
        self.article_count = Article.objects.all().count()
        self.comment = Comment.objects.create(article=self.article,
                                              author=self.user,
                                              contents='test comment')

    def test_article_list(self):
        response = self.client.get('/art/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_article_create(self):
        data = {
            'title': 'White',
            'category': self.category.id,
            'contents': 'leverage',
            'author': self.user
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/art/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Article.objects.all().count(), self.article_count + 1)

        new_article = Article.objects.latest('id')
        self.assertEqual(new_article.title, data['title'])

    def test_article_detail(self):
        response = self.client.get('/art/{0}/'.format(self.article.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Fractal is wonderful')

    def test_get_comment(self):
        response = self.client.get('/{0}/comments/'.format(self.article.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_comment(self):
        data = {
            'article': self.article.id,
            'contents': 'How calculus makes the world smarter',
            'author': self.user,
            'parent': self.comment.id
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/{0}/comments/'.format(self.article.id), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase, APIRequestFactory

from .models import *
from .views import *


User = get_user_model()


class NewsAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='username',
                                             password='password123',
                                             nickname='test_nickname')
        self.category = Category.objects.create(name='art')
        self.article = Article.objects.create(title='fractal',
                                              category=self.category,
                                              contents='fractal is wonderful',
                                              author=self.user)
        self.article_count = Article.objects.all().count()

    def test_article_list(self):
        response = self.client.get('/art/', format='json')
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

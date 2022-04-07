from datetime import date
from django.contrib.auth import get_user_model
from celery import shared_task
from .models import Category, Article

User = get_user_model()


@shared_task
def choose_article_every_midnight():
    try:
        categories = Category.objects.all()
        for category in categories:
            articles = Article.objects_sorted_by_vote.filter(
                category=category, date_posted__date=date.today())[:3]
            for article in articles:
                article.is_news = True
                article.save()
                user = User.objects.get(username=article.author)
                user.point += 50
                user.save()
    except ValueError as e:
        print(e)
    else:
        return 'success'


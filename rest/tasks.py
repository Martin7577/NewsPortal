from datetime import timezone, datetime

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


from celery import shared_task


from .models import Post, Category, Author, User


@shared_task
def send_mails(pk):
    post = Post.objects.get(pk=pk)
    categories = Category.objects.all()
    subscriber: list[str] = []
    subscriber_email = post.post_author.user.email

    for i in categories:
        subscribers = i.subscribers.all()
        for s in subscribers:
            if s.email != subscriber_email:
                subscriber.append(s.email)

    html_content = render_to_string(
        'post_created_email.html',
        {
            'small_text': post.preview(),
            'link': f'{settings.SITE_URL}/news/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject=post.header,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscriber,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()

@shared_task
def send_email_week():
    today = timezone.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(datetime_in__gte=last_week)
    categories = set(posts.values_list('category__name', flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers', flat=True))

    for user_id in subscribers:
        if user_id:
            user = User.objects.get(id=user_id)
            user_is_author = Author.objects.filter(user_id=user_id).exists()
            print(f'posts-{posts}')
            if user_is_author:
                postses = posts
                postses = postses.exclude(author=user.author)
                posts_ = set(postses)
            if posts_:
                html_content = render_to_string(
                    'daily_post.html',
                    {
                        'link': settings.SITE_URL,
                        'posts': posts_,

                    }
                )

                msg = EmailMultiAlternatives(
                    subject='новости за неделю',
                    body='',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[user.email],
                )

                msg.attach_alternative(html_content, 'text/html')
                msg.send()

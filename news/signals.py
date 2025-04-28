from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.urls import reverse
from django.template.loader import render_to_string
from allauth.account.signals import user_signed_up

from NewsPortal import settings
from .models import PostCategory


def send_notifications(preview, pk, title, subscribers):
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/news/{pk}',
        }
    )
    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs ):
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()
        subscribers_emails = []

        for cat in categories:
            subscribers = cat.subscribers.all()
            subscribers_emails += [s.email for s in subscribers]

        send_notifications(instance.preview(), instance.pk, instance.title, subscribers_emails)


@receiver(user_signed_up)
def send_welcome_email(request, user, **kwargs):
    # Формируем контекст для шаблона
    context = {
        'user': user,
        'site_url': settings.SITE_URL,
        'login_url': settings.SITE_URL + reverse('account_login')
    }

    # Рендерим HTML-содержимое
    email_html_message = render_to_string('account/email/welcome_email.html', context)
    email_plain_message = render_to_string('account/email/welcome_email.txt', context)

    # Отправляем письмо
    send_mail(
        subject='Добро пожаловать на NewsPortal!',
        message=email_plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=email_html_message,
        fail_silently=False,
    )
from django.db import models

from users.models import CustomUser


class Subscriber(models.Model):
    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    full_name = models.CharField(max_length=100, verbose_name='Ф.И.О.')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="subscribers")

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ['owner', ]

    def __str__(self):
        return self.full_name


class Message(models.Model):
    headline = models.CharField(max_length=100, verbose_name='Тема письма')
    body = models.TextField(verbose_name='Тело письма')
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="subscribers")

    class Meta:
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письмо'
        ordering = ['headline', ]

    def __str__(self):
        return self.headline


class Sending(models.Model):
    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('completed', 'Завершена'),
    ]
    start_time = models.DateTimeField(verbose_name='Дата и время начала рассылки')
    end_time = models.DateTimeField(verbose_name='Дата и время окончания рассылки')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='sending')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name="Статус", )
    subscribers = models.ManyToManyField(Subscriber, related_name='sending')
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="subscribers")

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ['start_time', ]


class SendAttempt(models.Model):

    STATUS_CHOICES = [
        ('successfully', 'Успешно'),
        ('not_successfully', 'Не успешно'),
    ]
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата и время рассылки')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name="Статус")
    response = models.TextField(verbose_name="Ответ почтового сервера")
    sending = models.ForeignKey(Sending, on_delete=models.CASCADE, related_name='sending_attempts')

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылки'
        ordering = ['created_at', ]

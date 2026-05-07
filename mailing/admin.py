from django.contrib import admin

from mailing.models import Message, Sending, Subscriber


@admin.register(Sending)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Subscriber)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Message)
class CategoryAdmin(admin.ModelAdmin):
    pass

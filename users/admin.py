from django.contrib import admin

from users.models import CustomUser


@admin.register(CustomUser)
class CategoryAdmin(admin.ModelAdmin):
    exclude = ("password",)

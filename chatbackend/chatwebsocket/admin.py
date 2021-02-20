from django.contrib import admin


from .models import *


@admin.register(User)
class ArticleAdmin(admin.ModelAdmin):

    list_display = ("name","channel") #ekranda görülecek özellikler
    class Meta:
        model: User


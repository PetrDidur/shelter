from django.contrib import admin

from dogs.models import Category, Dog


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'description')


@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'photo', 'birth_date')
    list_filter = ('category',)




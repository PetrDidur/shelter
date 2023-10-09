from django.urls import path

from dogs.apps import DogsConfig
from dogs.views import index, CategoryListView, DogListView, DogCreateView, DogDetailView, DogUpdateView, DogDeleteView

app_name = DogsConfig.name


urlpatterns = [
    path('', index, name='index'),
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('dogs/<int:pk>/', DogListView.as_view(), name='category'),
    path('dogs/create/', DogCreateView.as_view(), name='dog_create'),
    path('dogs/view/<int:pk>/', DogDetailView.as_view(), name='dog_detail'),
    path('dogs/edit/<int:pk>/', DogUpdateView.as_view(), name='dog_update'),
    path('dogs/delete/<int:pk>/', DogDeleteView.as_view(), name='dog_delete')
]
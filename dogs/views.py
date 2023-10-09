from datetime import datetime

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.cache import cache
from django.core.paginator import Paginator
from django.forms import inlineformset_factory
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from dogs.forms import DogForm, ParentForm
from dogs.models import Dog, Category, Parent
from dogs.services import get_categories_cache


@login_required
def index(request):
    objects_category = Category.objects.all()
    paginator = Paginator(objects_category, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    current_year = datetime.now().year

    context = {
        'object_list': get_categories_cache(),
        'title': 'Питомник - Наши породы',
        'page': page,
        'current_year': current_year
    }
    return render(request, 'dogs/index.html', context)


"""def categories(request):
    object_list = Category.objects.all()
    context = {
        'object_list': object_list,
        'title': 'Питомник - Наши породы'
    }

    return render(request, 'dogs/category_list.html', context)"""


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Питомник - Наши породы'
        return context


"""def dogs(request, pk):
    category_item = Category.objects.get(pk=pk)

    object_list = Dog.objects.filter(category_id=pk)

    context = {
        'object_list': object_list,
        'title': f'Наши собаки породы {category_item.name}'
    }

    return render(request, 'dogs/dog_list.html', context)"""


class DogListView(LoginRequiredMixin, ListView):
    model = Dog

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(category_id=self.kwargs.get('pk'))

        if not self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        category_item = Category.objects.get(pk=self.kwargs.get('pk'))
        context['title'] = f'Питомник - Наши породы {category_item.name}'
        return context


class DogCreateView(LoginRequiredMixin, PermissionRequiredMixin,  CreateView):
    model = Dog
    form_class = DogForm
    permission_required = 'dogs.add_dog'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        ParentFormSet = inlineformset_factory(Dog, Parent, form=ParentForm, extra=1)
        if self.request.method == 'POST':
            formset = ParentFormSet(self.request.POST, instance=self.object)
        else:
            formset = ParentFormSet(instance=self.object)

        context_data['formset'] = formset
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()

        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)

    success_url = reverse_lazy('dogs:index')


class DogDetailView(LoginRequiredMixin, DetailView):
    model = Dog


class DogUpdateView(LoginRequiredMixin, UpdateView):
    model = Dog
    form_class = DogForm

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise Http404
        return self.object

    def get_success_url(self):
        return reverse('dogs:dog_detail', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        ParentFormSet = inlineformset_factory(Dog, Parent, form=ParentForm, extra=1)
        if self.request.method == 'POST':
            formset = ParentFormSet(self.request.POST, instance=self.object)
        else:
            formset = ParentFormSet(instance=self.object)

        context_data['formset'] = formset
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()

        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)


class DogDeleteView(LoginRequiredMixin, DeleteView):
    model = Dog
    success_url = reverse_lazy('dogs:index')








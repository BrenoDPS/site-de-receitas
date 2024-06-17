from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Recipe
from . import models
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import json


@require_http_methods(["GET"])
def api_recipe_list(request):
    recipes = Recipe.objects.all().values('id', 'title', 'description', 'ingredientes', 'author__username', 'created_at', 'updated_at')
    return JsonResponse(list(recipes), safe=False)


@require_http_methods(["GET"])
def api_recipe_detail(request, pk):
    try:
        recipe = Recipe.objects.get(pk=pk)
        return JsonResponse({
            'id': recipe.id,
            'title': recipe.title,
            'description': recipe.description,
            'ingredientes': recipe.ingredientes,
            'author': recipe.author.username,
            'created_at': recipe.created_at,
            'updated_at': recipe.updated_at
        })
    except Recipe.DoesNotExist:
        return JsonResponse({'error': 'Recipe not found'}, status=404)


@csrf_exempt
@require_http_methods(["DELETE"])
def api_delete_recipe(request, pk):
    try:
        recipe = Recipe.objects.get(pk=pk)

        if request.user != recipe.author:
            return JsonResponse({'error': 'Permission denied'}, status=403)

        recipe.delete()
        return JsonResponse({'success': 'Recipe deleted'})
    except Recipe.DoesNotExist:
        return JsonResponse({'error': 'Recipe not found'}, status=404)


@csrf_exempt
@require_http_methods(["POST"])
def api_create_recipe(request):
    try:
        data = json.loads(request.body)
        title = data['title']
        description = data['description']
        author_id = data['author']
        author = User.objects.get(pk=author_id)

        recipe = Recipe.objects.create(
            title=title,
            description=description,
            author=author
        )
        return JsonResponse({
            'id': recipe.id,
            'title': recipe.title,
            'description': recipe.description,
            'ingredientes': recipe.ingredientes,
            'author': recipe.author.username,
            'created_at': recipe.created_at,
            'updated_at': recipe.updated_at
        }, status=201)
    except (json.JSONDecodeError, KeyError):
        return HttpResponseBadRequest('Invalid data')
    except User.DoesNotExist:
        return JsonResponse({'error': 'Author not found'}, status=404)


@csrf_exempt
@require_http_methods(["PUT"])
def api_update_recipe(request, pk):
    try:
        data = json.loads(request.body)
        recipe = Recipe.objects.get(pk=pk)

        if request.user != recipe.author:
            return JsonResponse({'error': 'Permission denied'}, status=403)

        recipe.title = data.get('title', recipe.title)
        recipe.description = data.get('description', recipe.description)
        recipe.save()

        return JsonResponse({
            'id': recipe.id,
            'title': recipe.title,
            'description': recipe.description,
            'ingredientes': recipe.ingredientes,
            'author': recipe.author.username,
            'created_at': recipe.created_at,
            'updated_at': recipe.updated_at
        })
    except Recipe.DoesNotExist:
        return JsonResponse({'error': 'Recipe not found'}, status=404)
    except json.JSONDecodeError:
        return HttpResponseBadRequest('Invalid data')
    

class RecipeListView(ListView):
  model = models.Recipe
  template_name = 'recipes/home.html'
  context_object_name = 'recipes'

# Create your views here.
def home(request):
  recipes = models.Recipe.objects.all()
  context = {
    'recipes': recipes
  }
  return render(request, 'recipes/home.html', context)

def about(request):
  return render(request, 'recipes/about.html', {'title': 'about page'})


class RecipeDetailView(DetailView):
  model = models.Recipe

class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
  model = models.Recipe
  success_url = reverse_lazy('recipes-home')

  def test_func(self):
    recipe = self.get_object()
    return self.request.user == recipe.author

class RecipeCreateView(LoginRequiredMixin, CreateView):
  model = models.Recipe
  fields = ['title', 'description']

  def form_valid(self, form):
    form.instance.author = self.request.user
    return super().form_valid(form)

class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
  model = models.Recipe
  fields = ['title', 'description']

  def test_func(self):
    recipe = self.get_object()
    return self.request.user == recipe.author

  def form_valid(self, form):
    form.instance.author = self.request.user
    return super().form_valid(form)
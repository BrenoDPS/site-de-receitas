from django.urls import path
from .views import (
    api_recipe_list, api_recipe_detail, api_create_recipe,
    api_update_recipe, api_delete_recipe
)
from . import views

urlpatterns = [
    path('', views.RecipeListView.as_view(), name="recipes-home"),
    path('recipe/<int:pk>', views.RecipeDetailView.as_view(), name="recipes-detail"),
    path('recipe/create', views.RecipeCreateView.as_view(), name="recipes-create"),
    path('recipe/<int:pk>/update', views.RecipeUpdateView.as_view(), name="recipes-update"),
    path('recipe/<int:pk>/delete', views.RecipeDeleteView.as_view(), name="recipes-delete"),
    path('about/', views.about, name="recipes-about"),
    # API views
    path('api/recipes/', api_recipe_list, name='api-recipe-list'),
    path('api/recipes/<int:pk>/', api_recipe_detail, name='api-recipe-detail'),
    path('api/recipes/create/', api_create_recipe, name='api-create-recipe'),
    path('api/recipes/<int:pk>/update/', api_update_recipe, name='api-update-recipe'),
    path('api/recipes/<int:pk>/delete/', api_delete_recipe, name='api-delete-recipe'),
]
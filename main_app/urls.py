from django.urls import path, include
from . import views


urlpatterns = [
    path('floors/', views.FloorListCreateView.as_view(), name='floor-list'),
    path('floors/<int:id>/', views.FloorDetailView.as_view(), name='floor-detail'),
    path('pantries/', views.PantryListCreateView.as_view(), name='pantry-list'),
    path('pantries/<int:id>/', views.PantryDetailView.as_view(), name='pantry-detail'),
    path('dispensers/', views.DispenserListCreateView.as_view(), name='dispenser-list'),
    path('dispensers/<int:id>/', views.DispenserDetailView.as_view(), name='dispenser-detail'),
    path('dispensers/<int:id>/update-level/', views.UpdateDispenserLevel.as_view(), name='update-dispenser-level'),
    path('users/register/', views.CreateUserView.as_view(), name='register'),
    path('users/login/', views.LoginView.as_view(), name='login'),
    path('users/token/refresh/', views.VerifyUserView.as_view(), name='token_refresh'),
]

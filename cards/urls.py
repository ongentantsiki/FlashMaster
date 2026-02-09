# cards/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Strona główna
    path('', views.home, name='home'),
    
    # Autentykacja (będzie w następnej sekcji)
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    
    # Talie
    path('decks/', views.deck_list, name='deck_list'),
    path('decks/new/', views.deck_create, name='deck_create'),
    path('decks/<int:deck_id>/', views.deck_detail, name='deck_detail'),
    path('decks/<int:deck_id>/edit/', views.deck_edit, name='deck_edit'),
    path('decks/<int:deck_id>/delete/', views.deck_delete, name='deck_delete'),
    
    # Fiszki 
    # Add path to create 'card' decks/<deck_id>/cards/create
    path('decks/<int:deck_id>/cards/create/', views.card_create, name='card_create'),
    path('cards/<int:card_id>/edit/', views.card_edit, name='card_edit'),
    path('cards/<int:card_id>/delete/', views.card_delete, name='card_delete'),
    path('decks/<int:deck_id>/cards/<int:card_id>/details/', views.card_detail, name='card_detail'),
    #path('cards/<int:card_id>/', views.card_detail, name='card_detail'),
    #path('decks/<int:deck_id>/cards/', views.card_list, name='card_list'),
    #path('decks/<int:deck_id>/cards/<int:card_id>/edit/', views.card_edit, name='card_edit'),
    #path('decks/<int:deck_id>/cards/<int:card_id>/delete/', views.card_delete, name='card_delete'),
]
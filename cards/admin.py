from django.contrib import admin
from .models import Deck, Card, Review

# Regestration of model Deck
@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    """Admin configuration for the Deck model."""
    list_display = ('name', 'owner', 'created_at') # pols from models.py for class Deck
    list_filter = ('owner', 'created_at') 
    search_fields = ('name',)

# Regestration of model Card
@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    """Admin configuration for the Card model."""
    list_display = ('front', 'deck', 'created_at')
    list_filter = ('deck', 'created_at')
    search_fields = ('front', 'back')


# Regestration of model Review
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Admin configuration for the Review model."""
    list_display = ('user', 'card', 'rating', 'reviewed_at')
    list_filter = ('user', 'rating', 'reviewed_at')
    search_fields = ('card__front', 'user__username')


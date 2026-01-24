from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Deck(models.Model):
    """
    Model representing a flashcard deck.
    
    Attributes:
        name: The name of the deck.
        owner: The user who owns the deck.
        created_at: The timestamp when the deck was created.
    """
   
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """Return the deck name"""
        return self.name

    class Meta:
        verbose_name = "Deck"
        verbose_name_plural = "Decks"


class Card(models.Model):
    """
    Model representing a flashcard.
    
    Attributes:
        deck: The deck this card belongs to.
        front: The question or front side of the flashcard.
        back: The answer or back side of the flashcard.
        created_at: The timestamp when the card was created.
    """
   
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    front = models.TextField(max_length=250)  # Pytanie / przód fiszki
    back = models.TextField(max_length= 250)   # Odpowiedź / tył fiszki
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """Return the front side of the card."""
        return f"{self.front[:50]}..."  # Pierwsze 50 znaków pytania

    class Meta:
        verbose_name = "Card"
        verbose_name_plural = "Cards"


class Review(models.Model):
    """
    Model representing a review/rating of a flashcard.
    
    Attributes:
        card: The card being reviewed.
        user: The user who reviewed the card.
        rating: The rating given to the card.
        reviewed_at: The timestamp when the review was created.
    """
    
    RATING_CHOICES = [
        (0, 'Don\'t know'),
        (1, 'Mediocre'),
        (2, 'Good'),
    ]
    
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES, default=0)
    reviewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """Return a string representation of the review."""
        return f"{self.user.username} - {self.card.front[:30]} - {self.get_rating_display()}"

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

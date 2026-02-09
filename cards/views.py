from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Deck, Card

# User views

def register_view(request):
    """Register a new user and automatically log them in."""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() # tworzy nowy 
            #redirect('login') mozemy kazac sie zalogowac, tj.przeniesc na strone login.html ktora korysta z ponizszego login_view
            login(request, user) # automatyczne logowanie po rejestracji
            return redirect('home') # try 'deck_list.html' insted of 'home.html'
    else:      
        form = UserCreationForm()
    return render(request, 'cards/register.html', {'form': form})

def login_view(request):
    """Authenticate and log in a user."""
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'cards/login.html', {'form': form}) # odswiezenie strony z loginem


def logout_view(request):
    """Log out the current user."""
    logout(request)
    return redirect('home')

def home(request):
    """Display the home page."""
    return render(request, 'cards/home.html')

# Deck views

@login_required
def deck_create(request):
    """
    Create a new deck for the current user.
   
    Handles both GET and POST requests:
    - GET: Display the deck creation form
    - POST: Process the submitted form and create a new deck owned by the user
    """
    if request.method == "POST":
        name = request.POST.get('name')
        deck = Deck.objects.create(
            name=name,
            owner=request.user
        )
        return redirect('deck_list')
    else:
        return render(request, 'cards/deck_form.html')

@login_required
def deck_delete(request, deck_id):
    """
    Delete a deck owned by the current user.
    
    Handles GET requests to display a confirmation page and POST requests to delete the deck.
    """
    deck = get_object_or_404(Deck, id=deck_id, owner=request.user)
    if request.method == "POST":
        deck.delete()
        return redirect('deck_list')
    return render(request, 'cards/deck_confirm_delete.html', {'deck': deck})


@login_required
def deck_edit(request, deck_id):
    """
    Edit an existing deck owned by the current user.
    """

    deck = get_object_or_404(Deck, id=deck_id, owner=request.user)
    if request.method == "POST":
        name = request.POST.get('name')
        deck.name = name
        deck.save()
        return redirect('deck_list')
    else:
        return render(request, 'cards/deck_form.html', {
            'deck': deck
        })

@login_required
def deck_list(request):
    """
    Display a list of all decks belonging to the current user.
   
    GET request handler that retrieves all decks owned by the logged-in user
    and displays them in a list view.
    """
    decks = Deck.objects.filter(owner=request.user).order_by('-created_at') # sorted from recent to oldest. by default is ascending order, so we add '-' to sort in descending order.
    return render(request, 'cards/deck_list.html', {
        'decks': decks,
    })

@login_required
def deck_detail(request, deck_id):
    """
    Display detailed information about a specific deck.
   
    Retrieves a deck by ID, ensuring it belongs to the current user.
    Returns 404 if the deck is not found or doesn't belong to the user.
    
    Args:
        request: The HTTP request object
        deck_id: The ID of the deck to display
    """
    if request.method == "POST":
        return redirect('card_create', deck_id = deck_id)  # Redirect to card creation page on POST request
    deck = get_object_or_404(Deck, id=deck_id, owner=request.user)
    return render(request, 'cards/deck_detail.html', {
        'deck': deck
    })

    
# Card views

@login_required
def card_create(request, deck_id):
    """Widok tworzenia fiszki"""
    deck_id = request.GET.get('deck')
    deck = None
    if deck_id:
        deck = get_object_or_404(Deck, id=deck_id, owner=request.user)
    
    if request.method == 'POST':
        deck_id = request.POST.get('deck')
        deck = get_object_or_404(Deck, id=deck_id, owner=request.user)
        front = request.POST.get('front')
        back = request.POST.get('back')
        if front and back:
            card = Card.objects.create(
                deck=deck,
                front=front,
                back=back
            )
            return redirect('deck_detail', deck_id=deck.id)
    
    decks = Deck.objects.filter(owner=request.user)
    return render(request, 'cards/card_form.html', {
        'deck': deck,
        'decks': decks
    })

@login_required
def card_delete(request, card_id):
    """
    Delete a card owned by the current user.

    Handles GET requests to display a confirmation page and POST requests to delete the card.
    """
    card = get_object_or_404(Card, id=card_id, owner=request.user)
    if request.method == "POST":
        card.delete()
        deck_id = card.deck.id
        return redirect('card_list', deck_id=deck_id)
    return render(request, 'cards/card_confirm_delete.html', {'card': card})

@login_required
def card_edit(request, card_id):
    """
    Edit an existing card owned by the current user.

    Handles both GET and POST requests:
    - GET: Display the card edit form
    - POST: Process the submitted form and update the card.
    """
    card = get_object_or_404(Card, id=card_id, owner=request.user)
    if request.method == "POST":
        name = request.POST.get('name')
        card.name = name
        card.save()
        return redirect('deck_list')
    else:
        return render(request, 'cards/card_form.html', {
            'card': card
        })

@login_required
def card_detail(request, card_id):
    """
    Display detailed information about a specific card.

    Retrieves a card by ID, ensuring it belongs to the current user.
    Returns 404 if the card is not found or doesn't belong to the user.
    
    Args:
        request: The HTTP request object
        card_id: The ID of the card to display
    """
    card = get_object_or_404(Card, id=card_id, owner=request.user)
    return render(request, 'cards/card_detail.html', {
        'card': card
    })
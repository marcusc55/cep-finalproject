from django.shortcuts import render
from django.http import Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
# Import the Category model
from gameangel.models import Game
from gameangel.models import Comment
#from gameangel.models import Catergory
from gameangel.forms import GameForm
from gameangel.forms import UserForm, UserProfileForm
from gameangel.forms import CommentForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required    

def encode_url(url):
    return url.replace(' ', '_')
  
def decode_url(url):
    return url.replace('_', ' ')

def get_game_list(max_results=0, starts_with=''):
    game_list = []
    if starts_with:
      game_list = Game.objects.filter(title__istartswith=starts_with) #changed from name__istartswith
    else:
      game_list = Game.objects.all()

    if max_results > 0:
      if len(game_list) > max_results:
        game_list = game_list[:max_results]

    for game in game_list:
        game.url = encode_url(game.title) #changed from game.name
    return game_list
 
def suggest_game(request):
    context = RequestContext(request)
    game_list = []
    starts_with = ''
    if request.method == 'POST':
        starts_with = request.POST['suggestion']

    game_list = get_game_list(8, starts_with)

    return render_to_response('gameangel/game_list.html', {'sw':starts_with,'game_list': game_list }, context)
     


def index(request):

    context = RequestContext(request)


    game_list = Game.objects.order_by('title')[:5]
    context_dict = {'Games': game_list}

 
    for game in game_list:
        game.url = game.title.replace(' ', '_')


    return render_to_response('gameangel/index.html', context_dict, context)
  
  
from gameangel.forms import GameForm
@login_required
def add_game(request):
    # Get the context from the request.
    context = RequestContext(request)

    # A HTTP POST?
    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES)  
        form.save(commit=False)
        # Have we been provided with a valid form?
        if form.is_valid():
            if 'icon' in request.FILES:
                form.icon = request.FILES['icon']
            if 'picture_1' in request.FILES:                                                   #need help
                form.picture = request.FILES['picture_1']
            if 'picture_2' in request.FILES:
                form.picture = request.FILES['picture_2']
            if 'picture_3' in request.FILES:
                form.picture = request.FILES['picture_3']
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return HttpResponseRedirect('/gameangel/')
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = GameForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render_to_response('gameangel/add_game.html', {'form': form}, context)
  


def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render_to_response(
            'gameangel/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)

def GameDetail(request, game_id):
    context = RequestContext(request)
    
    try:
      game1 = Game.objects.get(title=game_id)
      comments_list = []
      comments_list = Comment.objects.filter(game__title=game_id)
    except Game.DoesNotExist:
      raise Http404
      
    return render_to_response(
    'gameangel/gamedetail.html',
     {'Game':game1, 'comment_list':comments_list},
    context)

from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse  
def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']
        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)
        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            if user.is_active:  # Is the account active? It could have been disabled.
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/gameangel/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Game Angel account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")
    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('gameangel/login.html', {}, context)


# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/gameangel/')      
      
@login_required
def add_comment(request):
    # Get the context from the request.
    context = RequestContext(request)

    # A HTTP POST?
    if request.method == 'POST':
        form = CommentForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return HttpResponseRedirect('/gameangel/')
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = CommentForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render_to_response('gameangel/add_comment.html', {'form': form}, context)
  
@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")
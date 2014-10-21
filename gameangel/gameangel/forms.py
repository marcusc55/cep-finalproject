from django import forms
from gameangel.models import Game, User, UserProfile, Comment

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('email', 'picture')
        
class GameForm(forms.ModelForm):
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Game

        # What fields do we want to include in our form?
        # This way we don't need every field in the model present.
        # Some fields may allow NULL values, so we may not want to include them...
        # Here, we are hiding the foreign key.
        fields = ('title', 'icon', 'description', 'developer', 'picture_1', 'picture_2', 'picture_3', 'link',)
        
    def clean(self):
        cleaned_data = self.cleaned_data
        link = cleaned_data.get('link')

        # If link is not empty and doesn't start with 'http://', prepend 'http://'.
        if link and not link.startswith('https://'):
            link = 'https://' + link
            cleaned_data['link'] = link

        return cleaned_data
class CommentForm(forms.ModelForm):
  class Meta:
    model=Comment
    fields = ('author_alias','comment','game')
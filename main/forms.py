from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import SkillGroup, UserProfile, Skill, VideoGame, Tournament


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user



class SkillGroupForm(forms.ModelForm):
    class Meta:
        model = SkillGroup
        fields = ['name', 'description', 'owner']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError("Name is required.")
        return name


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio']


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'description', 'skill_group']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        self.fields['skill_group'].queryset = SkillGroup.objects.all()


class VideoGameForm(forms.ModelForm):
    class Meta:
        model = VideoGame
        fields = ["title", "description", "release_date"]


class AssignSkillGroupForm(forms.ModelForm):
    class Meta:
        model = VideoGame
        fields = ['required_skillgroup']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['required_skillgroup'].queryset = SkillGroup.objects.all()


class TournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ['name', 'description', 'date']





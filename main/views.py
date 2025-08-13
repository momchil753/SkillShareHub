from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import RegisterForm, SkillGroupForm, SkillForm, VideoGameForm, AssignSkillGroupForm, TournamentForm
from django.contrib.auth.forms import AuthenticationForm
from .models import SkillGroup, Skill, VideoGame, Tournament


class HomeView(TemplateView):
    template_name = "home.html"


@login_required
def dashboard(request):
    return render(request, "dashboard.html")


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("dashboard")
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("dashboard")
        messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("home")


class SkillGroupListView(ListView):
    model = SkillGroup
    template_name = 'skillgroup_list.html'
    context_object_name = 'skillgroups'


@method_decorator(login_required, name='dispatch')
class MySkillGroupsListView(ListView):
    model = SkillGroup
    template_name = 'skillgroup_list.html'  # reuse the All SkillGroups template
    context_object_name = 'skillgroups'

    def get_queryset(self):
        return SkillGroup.objects.filter(owner=self.request.user)


class SkillGroupDetailView(DetailView):
    model = SkillGroup
    template_name = 'skillgroup_detail.html'
    context_object_name = 'skillgroup'


class SkillGroupCreateView(LoginRequiredMixin, CreateView):
    model = SkillGroup
    form_class = SkillGroupForm
    template_name = 'skillgroup_form.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class SkillGroupUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = SkillGroup
    form_class = SkillGroupForm
    template_name = 'skillgroup_form.html'
    success_url = reverse_lazy('dashboard')

    def test_func(self):
        skillgroup = self.get_object()
        return self.request.user.is_superuser or skillgroup.owner == self.request.user


class SkillGroupDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = SkillGroup
    template_name = 'skillgroup_confirm_delete.html'
    success_url = reverse_lazy('dashboard')

    def test_func(self):
        skillgroup = self.get_object()
        return self.request.user.is_superuser or skillgroup.owner == self.request.user


class AllSkillsListView(LoginRequiredMixin, ListView):
    model = Skill
    template_name = "skills_all.html"
    context_object_name = "skills"
    ordering = ["-created_at"]


class MySkillsListView(LoginRequiredMixin, ListView):
    model = Skill
    template_name = "skills_mine.html"
    context_object_name = "skills"

    def get_queryset(self):
        return Skill.objects.filter(created_by=self.request.user).order_by("-created_at")


class SkillCreateView(LoginRequiredMixin, CreateView):
    model = Skill
    form_class = SkillForm
    template_name = 'skill_form.html'
    success_url = reverse_lazy('skills_mine')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class SkillUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Skill
    form_class = SkillForm
    template_name = "skill_form.html"
    success_url = reverse_lazy("dashboard")

    def test_func(self):
        skill = self.get_object()
        return self.request.user.is_superuser or skill.created_by == self.request.user

    def dispatch(self, request, *args, **kwargs):
        skill = self.get_object()
        if not request.user.is_superuser and skill.created_by != request.user:
            return HttpResponseForbidden("You are not allowed to edit this skill.")
        return super().dispatch(request, *args, **kwargs)


class SkillDeleteView(LoginRequiredMixin, DeleteView):
    model = Skill
    template_name = 'skill_confirm_delete.html'
    success_url = reverse_lazy('skills_all')

    def dispatch(self, request, *args, **kwargs):
        skill = self.get_object()
        if not request.user.is_superuser and skill.created_by != request.user:
            return HttpResponseForbidden("You are not allowed to delete this skill.")
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(request, f'Skill "{self.get_object().name}" has been deleted.')
        return super().delete(request, *args, **kwargs)


class VideoGameListView(ListView):
    model = VideoGame
    template_name = "videogame_list.html"
    context_object_name = "games"


class VideoGameCreateView(LoginRequiredMixin, CreateView):
    model = VideoGame
    form_class = VideoGameForm
    template_name = "videogame_form.html"
    success_url = reverse_lazy("videogame_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class VideoGameUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = VideoGame
    form_class = VideoGameForm
    template_name = "videogame_form.html"
    success_url = reverse_lazy("videogame_list")

    def test_func(self):
        game = self.get_object()
        return self.request.user.is_superuser or game.created_by == self.request.user


class VideoGameDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = VideoGame
    template_name = "videogame_confirm_delete.html"
    success_url = reverse_lazy("videogame_list")

    def test_func(self):
        game = self.get_object()
        return self.request.user.is_superuser or game.created_by == self.request.user


class MyVideoGamesListView(LoginRequiredMixin, ListView):
    model = VideoGame
    template_name = "videogame_mine.html"
    context_object_name = "games"

    def get_queryset(self):
        return VideoGame.objects.filter(created_by=self.request.user)


class AssignSkillGroupView(LoginRequiredMixin, UpdateView):
    model = VideoGame
    form_class = AssignSkillGroupForm
    template_name = "assign_skillgroup.html"
    success_url = reverse_lazy("videogame_list")


class TournamentListView(ListView):
    model = Tournament
    template_name = "tournament_list.html"
    context_object_name = "tournaments"


class TournamentCreateView(LoginRequiredMixin, CreateView):
    model = Tournament
    form_class = TournamentForm
    template_name = "tournament_form.html"
    success_url = reverse_lazy("tournament_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    # redirect to register page if not logged in
    login_url = '/register/'


class TournamentDetailView(DetailView):
    model = Tournament
    template_name = "tournament_detail.html"
    context_object_name = "tournament"


class TournamentUpdateView(LoginRequiredMixin, UpdateView):
    model = Tournament
    form_class = TournamentForm
    template_name = "tournament_form.html"
    success_url = reverse_lazy("tournament_detail")


class TournamentDeleteView(LoginRequiredMixin, DeleteView):
    model = Tournament
    template_name = "tournament_confirm_delete.html"
    success_url = reverse_lazy("tournament_list")


def tournament_going(request, pk):
    tournament = get_object_or_404(Tournament, pk=pk)

    if request.user.is_authenticated:
        if request.user in tournament.going_users.all():
            tournament.going_users.remove(request.user)
        else:
            tournament.going_users.add(request.user)
            tournament.not_going_users.remove(request.user)
    return redirect("tournament_list")


def tournament_not_going(request, pk):
    tournament = get_object_or_404(Tournament, pk=pk)

    if request.user.is_authenticated:
        if request.user in tournament.not_going_users.all():
            tournament.not_going_users.remove(request.user)
        else:
            tournament.not_going_users.add(request.user)
            tournament.going_users.remove(request.user)
    return redirect("tournament_list")


class MyTournamentsListView(LoginRequiredMixin, ListView):
    model = Tournament
    template_name = "tournaments_mine.html"
    context_object_name = "tournaments"

    def get_queryset(self):
        return Tournament.objects.filter(created_by=self.request.user)


from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),

    # SkillGroups
    path('skillgroups/', views.SkillGroupListView.as_view(), name='skillgroup_list'),
    path('skillgroups/<int:pk>/', views.SkillGroupDetailView.as_view(), name='skillgroup_detail'),
    path('skillgroups/create/', views.SkillGroupCreateView.as_view(), name='skillgroup_create'),
    path('skillgroups/<int:pk>/edit/', views.SkillGroupUpdateView.as_view(), name='skillgroup_update'),
    path('skillgroups/<int:pk>/delete/', views.SkillGroupDeleteView.as_view(), name='skillgroup_delete'),
    path('skillgroups/mine/', views.MySkillGroupsListView.as_view(), name='skillgroup_mine'),


    # Skills
    path('skills/all/', views.AllSkillsListView.as_view(), name='skills_all'),
    path('skills/mine/', views.MySkillsListView.as_view(), name='skills_mine'),
    path('skills/create/', views.SkillCreateView.as_view(), name='skill_create'),
    path('skills/<int:pk>/edit/', views.SkillUpdateView.as_view(), name='skill_edit'),
    path('skills/<int:pk>/delete/', views.SkillDeleteView.as_view(), name='skill_delete'),

    # VideoGames
    path('games/', views.VideoGameListView.as_view(), name='videogame_list'),
    path('games/create/', views.VideoGameCreateView.as_view(), name='videogame_create'),
    path('games/<int:pk>/edit/', views.VideoGameUpdateView.as_view(), name='videogame_edit'),
    path('games/<int:pk>/delete/', views.VideoGameDeleteView.as_view(), name='videogame_delete'),
    path('games/mine/', views.MyVideoGamesListView.as_view(), name='videogame_mine'),
    path('games/<int:pk>/assign-skillgroup/', views.AssignSkillGroupView.as_view(), name='assign_skillgroup'),

    # Tournaments
    path('tournaments/', views.TournamentListView.as_view(), name='tournament_list'),
    path('tournaments/create/', views.TournamentCreateView.as_view(), name='tournament_create'),
    path('tournaments/<int:pk>/edit/', views.TournamentUpdateView.as_view(), name='tournament_update'),
    path('tournaments/<int:pk>/delete/', views.TournamentDeleteView.as_view(), name='tournament_delete'),
    path('tournaments/<int:pk>/going/', views.tournament_going, name='tournament_going'),
    path('tournaments/<int:pk>/not-going/', views.tournament_not_going, name='tournament_not_going'),
    path("tournaments/<int:pk>/", views.TournamentDetailView.as_view(), name="tournament_detail"),
    path('tournaments/mine/', views.MyTournamentsListView.as_view(), name='tournaments_mine'),
]


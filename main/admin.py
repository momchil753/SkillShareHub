from django.contrib import admin
from .models import UserProfile, SkillGroup, VideoGame, Skill, Tournament


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')
    search_fields = ('user__username',)


@admin.register(SkillGroup)
class SkillGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner')
    search_fields = ('name', 'owner__username')
    list_filter = ('owner',)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'skill_group')
    search_fields = ('skill_group', 'name')


@admin.register(VideoGame)
class VideoGameAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'release_date', 'required_skillgroup')
    search_fields = ('title', 'created_by__username')
    list_filter = ('created_by',)


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'date', 'created_by')
    search_fields = ('name', 'created_by','date')
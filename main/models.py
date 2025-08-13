from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"


class SkillGroup(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skillgroups', null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    skill_group = models.ForeignKey(
        'SkillGroup',
        on_delete=models.CASCADE,
        related_name='skills',
        null=True,
        blank=True
    )
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skills')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class VideoGame(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    release_date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    required_skillgroup = models.ForeignKey(
        'SkillGroup', on_delete=models.SET_NULL, null=True, blank=True, related_name="games"
    )

    def __str__(self):
        return self.title


class Tournament(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    going_users = models.ManyToManyField(User, related_name="tournaments_going", blank=True)
    not_going_users = models.ManyToManyField(User, related_name="tournaments_not_going", blank=True)

    def __str__(self):
        return self.name


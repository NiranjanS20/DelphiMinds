from django.db import models
from django.conf import settings

# Create your models here.


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class UserSkill(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='user_skills')
    level = models.PositiveIntegerField(default=0)  # 0-100
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'skill')

    def __str__(self):
        return f"{self.user.username} - {self.skill.name}: {self.level}"

from django.db import models
from django.conf import settings


class JobMarketData(models.Model):
    skill = models.ForeignKey('skills.Skill', on_delete=models.CASCADE, related_name='market_data')
    demand_score = models.FloatField(default=0.0)  # 0-100
    salary_range_min = models.IntegerField(default=0)
    salary_range_max = models.IntegerField(default=0)
    job_openings = models.IntegerField(default=0)
    growth_rate = models.FloatField(default=0.0)  # percentage
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-demand_score']

    def __str__(self):
        return f"{self.skill.name} - Demand: {self.demand_score}"


class IndustryTrend(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    growth_rate = models.FloatField(default=0.0)
    avg_salary = models.IntegerField(default=0)
    skills_in_demand = models.ManyToManyField('skills.Skill', related_name='trending_industries')
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
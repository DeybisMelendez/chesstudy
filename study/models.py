from django.db import models
from django.contrib.auth.models import User


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    elo_rating = models.IntegerField(default=1000)

    def __str__(self):
        return self.user.username


class EloHistory(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    elo_rating = models.IntegerField()
    result = models.FloatField()
    elo_variation = models.IntegerField()

    def __str__(self):
        return f"{self.player.user.username}'s Elo History"


class StudyTopic(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class StudyTopicPreferences(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    study_topic = models.ForeignKey(StudyTopic, on_delete=models.CASCADE)
    weekly_minutes_goal = models.IntegerField(default=120)

    def __str__(self):
        return f"{self.player.user.username} - {self.study_topic.name} - {self.weekly_minutes_goal} mins"

    class Meta:
        unique_together = ('player', 'study_topic')


class DailyProgress(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    study_topic = models.ForeignKey(StudyTopic, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    minutes_studied = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.player.user.username} - {self.study_topic.name}"

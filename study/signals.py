from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Player, StudyTopic, StudyTopicPreferences


@receiver(post_save, sender=User)
def create_player_profile(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)


@receiver(post_save, sender=Player)
def create_study_topic_preferences(sender, instance, created, **kwargs):
    if created:
        topics = StudyTopic.objects.all()
        for topic in topics:
            StudyTopicPreferences.objects.create(
                player=instance, study_topic=topic)

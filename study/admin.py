from django.contrib import admin
from .models import Player, EloHistory, StudyTopic, StudyTopicPreferences, DailyProgress
# Register your models here.
admin.site.register(Player)
admin.site.register(EloHistory)
admin.site.register(StudyTopic)
admin.site.register(StudyTopicPreferences)
admin.site.register(DailyProgress)

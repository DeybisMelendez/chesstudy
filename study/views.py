from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta
from .models import StudyTopic, DailyProgress, StudyTopicPreferences, Player, EloHistory
from django.contrib.auth.views import LoginView


class CustomLoginView(LoginView):
    template_name = 'login.html'


@login_required
def player_dashboard(request):
    today = date.today()
    player = request.user.player
    elo_history = EloHistory.objects.filter(
        player=player).order_by('-date')
    hightest_elo_history = EloHistory.objects.filter(
        player=player).order_by('-elo_rating')
    last_elo = elo_history[1] if elo_history else 0
    hightest_elo = hightest_elo_history[0] if hightest_elo_history else 0
    current_week_start = today - timedelta(days=date.today().weekday())
    current_week_end = current_week_start + \
        timedelta(days=6) + timedelta(hours=23) + timedelta(minutes=59)

    daily_progress = DailyProgress.objects.filter(
        player=player, date__gte=current_week_start, date__lte=current_week_end).order_by('-date')
    preferences = StudyTopicPreferences.objects.filter(player=player)
    minutes_studied_by_topic = {}
    study_data = []

    for progress in daily_progress:
        topic_name = progress.study_topic.name
        if topic_name not in minutes_studied_by_topic:
            minutes_studied_by_topic[topic_name] = progress.minutes_studied
        else:
            minutes_studied_by_topic[topic_name] += progress.minutes_studied

    for preference in preferences:
        topic_name = preference.study_topic.name
        weekly_goal = preference.weekly_minutes_goal
        minutes_studied = minutes_studied_by_topic.get(topic_name, 0)
        study_data.append(
            {'topic_name': topic_name, 'weekly_goal': weekly_goal, 'minutes_studied': minutes_studied, "progress": minutes_studied/weekly_goal})

    if request.method == "POST":
        study_topic_id = request.POST.get("study_topic")
        minutes_studied = int(request.POST.get("minutes_studied"))

        if StudyTopic.objects.filter(id=study_topic_id).exists() and 0 <= minutes_studied <= 1440:
            DailyProgress.objects.create(
                player=player, study_topic_id=study_topic_id, date=today, minutes_studied=minutes_studied)

    context = {
        "player": player,
        "current_week_start": current_week_start,
        "current_week_end": current_week_end,
        "study_data": study_data,
        "preferences": preferences,
        "history": daily_progress,
        "last_elo": last_elo,
        "hightest_elo": hightest_elo
    }

    return render(request, 'player_dashboard.html', context)


@login_required
def preferences(request):
    player = request.user.player
    preferences = StudyTopicPreferences.objects.filter(player=player)
    if request.method == 'POST':
        study_topic_id = request.POST.get("study_topic")
        minutes_goal = request.POST.get("minutes_goal")
        if StudyTopicPreferences.objects.filter(study_topic=study_topic_id).exists():
            study_topic_preference = StudyTopicPreferences.objects.get(
                player=player, study_topic_id=study_topic_id)
            study_topic_preference.weekly_minutes_goal = minutes_goal
            study_topic_preference.save()
    context = {
        "player": player,
        "preferences": preferences,
    }
    return render(request, 'preferences.html', context)


def top_elo(request):
    top_players = Player.objects.order_by('-elo_rating')

    context = {
        'top_players': top_players
    }

    return render(request, 'top_elo.html', context)

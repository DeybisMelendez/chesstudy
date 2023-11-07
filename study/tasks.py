from datetime import date, timedelta
from .models import Player
from .models import Player, EloHistory, StudyTopicPreferences, DailyProgress
from django.db.models import Sum


def update_elo():
    players = Player.objects.all()
    for player in players:
        # Se espera que el jugador cumpla con el 60% del objetivo.
        expected_score = 0.6
        study_preferences = StudyTopicPreferences.objects.filter(
            player=player)
        total_minutes_weekly_goal = sum(
            preference.weekly_minutes_goal for preference in study_preferences)
        k_constant = total_minutes_weekly_goal/60
        if k_constant >= 25:
            k_constant = 40
        elif k_constant >= 20:
            k_constant = 30
        elif k_constant >= 10:
            k_constant = 20
        else:
            k_constant = 12

        today = date.today()

        a_week_ago = today - timedelta(days=7)

        daily_progress_last_week = DailyProgress.objects.filter(
            player=player,
            date__range=(a_week_ago, today)
        )

        total_minutes_studied_last_week = float(sum(
            daily_progress.minutes_studied for daily_progress in daily_progress_last_week))
        score = total_minutes_studied_last_week/total_minutes_weekly_goal
        elo_var = int(k_constant * (score - expected_score))
        # Calcular el nuevo Elo
        player.elo_rating += elo_var
        player.save()

        # Crear un registro en la tabla EloHistory
        EloHistory.objects.create(
            player=player, elo_rating=player.elo_rating, elo_variation=elo_var, result=score)

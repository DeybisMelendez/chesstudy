from django.urls import path
from .views import player_dashboard, CustomLoginView, top_elo, preferences
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),
    path('dashboard/', player_dashboard, name='dashboard'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('top-elo/', top_elo, name='top_elo'),
    path('preferences/', preferences, name='preferences'),
]

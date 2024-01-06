from django.urls import path


from mastermind.api import views


app_name = 'api'


urlpatterns = [
    path('game-handler', views.GameHandlerView.as_view(), name='game_handler'),
    path('guess-handler/<uuid:game_id>', views.GuessHandlerView.as_view(), name='guess_handler'),
]

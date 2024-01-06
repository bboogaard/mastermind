from django.urls import include, path

from mastermind import views


app_name = 'mastermind'


urlpatterns = [
    path('', views.GameView.as_view(), name='game'),
    path('api/', include('mastermind.api.urls', namespace='api')),
]

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from mastermind.api import serializers
from mastermind.api.mixins import PlayerMixin
from mastermind.models import Game


class GameHandlerView(PlayerMixin, GenericAPIView):

    serializer_class = serializers.GameSerializer

    def post(self, request, *args, **kwargs):
        game, created = Game.objects.get_or_create_latest(self.player)
        serializer = self.get_serializer(instance=game)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


class GuessHandlerView(GenericAPIView):

    serializer_class = serializers.GameSerializer

    def dispatch(self, request, game_id, *args, **kwargs):
        self.game = get_object_or_404(Game, game_id=game_id)
        return super().dispatch(request, *args, **kwargs)

    def get_serializer_context(self):
        return {
            'game': self.game
        }

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(instance=self.game)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        guess_serializer = serializers.GuessSerializer(data=request.data, context={'game': self.game})
        guess_serializer.is_valid(raise_exception=True)
        guess_serializer.save()
        serializer = self.get_serializer(instance=self.game)
        return Response(serializer.data)

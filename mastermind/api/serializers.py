from django.db.models import Max
from django.urls import reverse
from rest_framework import serializers

from mastermind.game import GameHandlerFactory
from mastermind.models import Game, Guess


class GameSerializer(serializers.ModelSerializer):

    guess_handler_url = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = ('game_id', 'guess_handler_url', 'is_active')

    def get_guess_handler_url(self, obj):
        return reverse('mastermind:api:guess_handler', args=[obj.game_id])

    def to_representation(self, instance):
        result = super().to_representation(instance)
        result['guesses'] = [
            {
                'code': guess.code,
                'hint': guess.hint,
                'position': guess.position
            }
            for guess in instance.guesses.all()
        ]
        result['code'] = instance.code if not instance.is_active else None
        result['code_broken'] = instance.code_broken
        results = list(
            instance.player.games.filter(is_active=False).with_result().values_list('code_broken', flat=True)
        )
        result['score'] = results.count(True), results.count(False)
        return result


class GuessSerializer(serializers.ModelSerializer):

    class Meta:
        model = Guess
        fields = ('code',)

    @property
    def game(self):
        return self.context.get('game')

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        data['position'] = (Guess.objects.filter(game=self.game).aggregate(
            max_position=Max('position')
        )['max_position'] or 0) + 1
        data['hint'] = GameHandlerFactory.create(self.game).check_code(data['code'])
        return data

    def create(self, validated_data):
        instance = Guess.objects.create(
            game=self.game,
            **validated_data
        )
        if self.game.guesses.count() == 12 or self.game.code_broken:
            self.game.is_active = False
            self.game.save()
        return instance

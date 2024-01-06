import random
import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models

from mastermind.fields import ColorField


class Player(models.Model):

    player_id = models.UUIDField()

    class Meta:
        ordering = ('player_id',)

    def __str__(self):
        return str(self.player_id)


def generate_game_id():
    return uuid.uuid4()


def generate_code():
    return [
        random.choice(ColorField.ColorChoices.choices)[0]
        for _ in range(4)
    ]


class GameQuerySet(models.QuerySet):

    def get_or_create_latest(self, player):
        return self.get_or_create(player=player, is_active=True)

    def with_result(self):
        qs = self._clone()
        return qs.annotate(
            code_broken=models.Exists(
                Guess.objects.filter(
                    game__pk=models.OuterRef('pk'),
                    code=models.OuterRef('code')
                )
            )
        )


class Game(models.Model):

    game_id = models.UUIDField(default=generate_game_id)

    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='games')

    code = ArrayField(ColorField(), size=4, default=generate_code)

    is_active = models.BooleanField(default=False)

    objects = GameQuerySet.as_manager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('player', 'is_active',),
                name='Unique constraint on player and is_active = true',
                condition=models.Q(is_active=True)
            )
        ]
        ordering = ('player',)

    def __str__(self):
        return str(self.game_id)

    @property
    def code_broken(self):
        return self.guesses.filter(code=self.code).exists()


class Guess(models.Model):

    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='guesses')

    position = models.PositiveIntegerField(default=0)

    code = ArrayField(ColorField(), size=4)

    hint = ArrayField(models.PositiveIntegerField(), size=2)

    class Meta:
        ordering = ('game', 'position')

    def __str__(self):
        return f'{self.game} - {self.position}'

from typing import List, Tuple

from mastermind.models import Game


class GameHandler:

    game: Game

    def __init__(self, game: Game):
        self.game = game

    def check_code(self, code: List[str]) -> Tuple[int, int]:
        position_ok = 0
        color_ok = 0
        colors = self.game.code[:]
        for pos, color in enumerate(code):
            try:
                index = colors.index(color)
                if index == pos:
                    position_ok += 1
                else:
                    color_ok += 1
                colors[index] = ''
            except ValueError:
                ...
        return position_ok, color_ok


class GameHandlerFactory:

    @classmethod
    def create(cls, game: Game):
        return GameHandler(game)

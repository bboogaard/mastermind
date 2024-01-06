from rest_framework.exceptions import NotFound
from rest_framework.views import APIView

from mastermind.models import Player
from mastermind.session import get_player_id_from_request


class PlayerMixin(APIView):

    @property
    def player(self):
        player_id = get_player_id_from_request(self.request)
        try:
            return Player.objects.get(player_id=player_id)
        except Player.DoesNotExist:
            raise NotFound()

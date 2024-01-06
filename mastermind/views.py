from django.views.generic import TemplateView

from mastermind.models import Player
from mastermind.session import get_player_id_from_request


class GameView(TemplateView):

    template_name = 'game.html'

    def get(self, request, *args, **kwargs):
        player_id = get_player_id_from_request(request)
        Player.objects.get_or_create(player_id=player_id)
        context = self.get_context_data()
        return self.render_to_response(context)

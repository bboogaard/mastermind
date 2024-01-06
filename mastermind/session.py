import uuid

from django.http import HttpRequest


SESSION_KEY = 'mastermind-player'


def get_player_id_from_request(request: HttpRequest):
    return request.session.setdefault(SESSION_KEY, str(uuid.uuid4()))

from django_webtest import WebTest
from django.urls import reverse

from mastermind.models import Player


class TestViews(WebTest):

    def test_all_guess_right(self):
        response = self.app.get(reverse('mastermind:game'))
        self.assertEqual(response.status_code, 200)
        response.mustcontain('Start/Resume game')

        player = Player.objects.first()
        self.assertIsNotNone(player)

        response = self.app.post(reverse('mastermind:api:game_handler'))
        self.assertEqual(response.status_code, 201)

        game = player.games.first()
        self.assertIsNotNone(game)
        game.code = ["blue", "red", "white", "yellow"]
        game.save()

        data = {
            'code': ["red", "black", "yellow", "white"]
        }
        response = self.app.post_json(reverse('mastermind:api:guess_handler', args=[game.game_id]), data)
        self.assertEqual(response.status_code, 200)
        result = response.json
        guesses = result['guesses']
        self.assertEqual(len(guesses), 1)
        guess = guesses[0]
        self.assertEqual(guess['hint'], [0, 3])

        data = {
            'code': ["black", "red", "yellow", "green"]
        }
        response = self.app.post_json(reverse('mastermind:api:guess_handler', args=[game.game_id]), data)
        self.assertEqual(response.status_code, 200)
        result = response.json
        guesses = result['guesses']
        self.assertEqual(len(guesses), 2)
        guess = guesses[1]
        self.assertEqual(guess['hint'], [1, 1])

        data = {
            'code': ["white", "red", "black", "yellow"]
        }
        response = self.app.post_json(reverse('mastermind:api:guess_handler', args=[game.game_id]), data)
        self.assertEqual(response.status_code, 200)
        result = response.json
        guesses = result['guesses']
        self.assertEqual(len(guesses), 3)
        guess = guesses[2]
        self.assertEqual(guess['hint'], [2, 1])

        data = {
            'code': ["blue", "red", "white", "yellow"]
        }
        response = self.app.post_json(reverse('mastermind:api:guess_handler', args=[game.game_id]), data)
        self.assertEqual(response.status_code, 200)
        result = response.json
        guesses = result['guesses']
        self.assertEqual(len(guesses), 4)
        self.assertEqual(result['codeBroken'], True)
        self.assertEqual(result['score'], [1, 0])

    def test_all_guess_wrong(self):
        response = self.app.get(reverse('mastermind:game'))
        self.assertEqual(response.status_code, 200)
        response.mustcontain('Start/Resume game')

        player = Player.objects.first()
        self.assertIsNotNone(player)

        response = self.app.post(reverse('mastermind:api:game_handler'))
        self.assertEqual(response.status_code, 201)

        game = player.games.first()
        self.assertIsNotNone(game)
        game.code = ["blue", "red", "white", "yellow"]
        game.save()

        data = {
            'code': ["red", "black", "yellow", "white"]
        }
        for _ in range(12):
            response = self.app.post_json(reverse('mastermind:api:guess_handler', args=[game.game_id]), data)
        self.assertEqual(response.status_code, 200)
        result = response.json
        guesses = result['guesses']
        self.assertEqual(len(guesses), 12)
        self.assertEqual(result['codeBroken'], False)
        self.assertEqual(result['score'], [0, 1])

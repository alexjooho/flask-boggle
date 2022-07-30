from unittest import TestCase

from app import app, games

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            response = client.get('/')

            html = response.get_data(as_text=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn('<table', html)  # doesn't check whole tag, but just for this part of it
            # test that you're getting a template
            # don't want to put whole table class = "board" because someone might change it
            # could even put in the comment since no one will change

    def test_api_new_game(self):
        """Test starting a new game."""

        with self.client as client:
            response = client.post("/api/new-game")
            html = response.get_data(as_text=True) #change, we're trying to check for gameId in games
            #need the .get_data to get the data part, and we need as_text=True because it is originally in byte string

            parsed = response.get_json() #must parse byte string into dictionary/object (can't parse text)
            self.assertIn("gameId", html)
            self.assertTrue(type(parsed["board"][0]) == list)
            self.assertTrue(games)
            #new assertion, type of gameId is string

    def test_score_word(self):
        """ test scoring a word """

        with self.client as client:
            response = client.post('/api/new-game')
            # html = response.get_data(as_text=True)

            parsed = response.get_json()
            gameId = parsed["gameId"]
            games[gameId].board = [
                ['C', 'A', 'T', 'A', 'A'],
                ['A', 'A', 'A', 'A', 'A'],
                ['A', 'A', 'A', 'A', 'A'],
                ['A', 'A', 'A', 'A', 'A'],
                ['A', 'A', 'A', 'A', 'A']
                ]

            score_response = client.post('/api/score-word', json = {"gameId": gameId, "word": "CAT"})  #need to do json = because it is testing an AJAX request
            score_response2 = client.post('/api/score-word', json = {"gameId": gameId, "word": "DOG"})
            score_response3 = client.post('/api/score-word', json = {"gameId": gameId, "word": "ABARC"})

                #make better variable names

            json_response = score_response.get_json()  #score_response gives us a byte string (JSON), we then turn this into dictionary
            json_response2 = score_response2.get_json()
            json_response3 = score_response3.get_json()
                #maybe call response_data because it's technically not json

            self.assertEqual(json_response, {"result": "ok"})
            self.assertEqual(json_response2, {"result": "not-on-board"})
            self.assertEqual(json_response3, {"result": "not-word"})

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
            html = response.get_data(as_text=True)

            parsed = response.get_json() #must parse byte string
            breakpoint()
            self.assertIn("gameId", html)
            self.assertTrue(type(parsed["board"][0]) == list)
            self.assertTrue(games)


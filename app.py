from flask import Flask, request, render_template, jsonify
from uuid import uuid4

from boggle import BoggleGame

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

# The boggle games created, keyed by game id
games = {}  # want to keep this out of an API database because we don't want to keep track of every game


@app.get("/")
def homepage():
    """Show board."""

    return render_template("index.html")


@app.post("/api/new-game")
def new_game():
    """Start a new game and return JSON: {game_id, board}."""

    # get a unique string id for the board we're creating
    game_id = str(uuid4())
    game = BoggleGame()
    games[game_id] = game

    return jsonify({"gameId": game_id, "board": game.board})


@app.post("/api/score-word")  # tested this with insomnia (more intuitive than console)
def score_word():
    """ Accepts word and gameId, returns a JSON saying if the word is legal """ #make sure for docstrings, include accepts and returns
    data = request.json # turns json into dictionary format, don't need .get_json()
            # needed to do .upper() for this because they might put in lower case words
    word = data["word"]
    gameId = data["gameId"]

    #breakpoint only works if server is up and api called

    if not games[gameId].is_word_in_word_list(word):
        return jsonify(result = "not-word")
    elif not games[gameId].check_word_on_board(word):
        return jsonify(result = "not-on-board")
    else:
        # call score word method
        games[gameId].play_and_score_word(word)  
        #added this so that it would play and score the word (although it doesn't matter yet)
        return jsonify(result= "ok")

from boggle import Boggle
from flask import *
import json

app = Flask(__name__)
app.config["SECRET_KEY"] ="EDFEHG^#T^3rty376gcdaw2"

boggle_game = Boggle()

@app.route('/')
def home():
    """Shows home screen"""
    return render_template('home.html')

@app.route('/game')
def game():
    """Initializes game by setting up high score, board, and found list"""
    if session.get('high_score'):
        high_score = session['high_score']
    else:
        session['high_score'] = 0
        high_score = 0

    board = boggle_game.make_board()
    found = list()
    session['found'] = found
    session['board'] = board
    return render_template('game.html', board=board, high_score=high_score)
    
@app.route('/guess')
def check_guess():
    """Checks submitted guess and returns a boolean"""
    board = session['board']
    guess = request.args['guess']
    on_board = boggle_game.check_valid_word(board, guess)
    found = bool(guess in session['found'])
    data = {'on_board': on_board, 'found': found}
    return data

@app.route('/found', methods=["POST"])
def found_word():
    """Adds guess to the found list"""
    found = json.loads(request.data)['guess']
    new = session['found']
    new.append(found)
    session['found'] = new
    return found

@app.route('/end-game')
def end_game():
    """Counts up the number of plays and returns the high score"""
    score = int(request.args[' score'])
    print('***********************************')
    print(request.args)
    print('***********************************')
    if session.get('num_plays'):
        session['num_plays'] += 1
    else:
        session['num_plays'] = 1

    num_plays = session['num_plays']

    if score > session['high_score']:
        session['high_score'] = score
    high_score = session['high_score']
    return {"high_score": high_score, 'num_plays': num_plays}
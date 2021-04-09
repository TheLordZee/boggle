from boggle import Boggle
from flask import *

app = Flask(__name__)
app.config["SECRET_KEY"] ="EDFEHG^#T^3rty376gcdaw2"

boggle_game = Boggle()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/game')
def game():
    if session.get('high_score'):
        high_score = session['high_score']
    else:
        session['high_score'] = 0
        high_score = 0

    board = boggle_game.make_board()
    session['board'] = board
    return render_template('game.html', board=board, high_score=high_score)
    
@app.route('/guess')
def check_guess():
    board = session['board']
    guess = request.args['guess']
    return boggle_game.check_valid_word(board, guess)
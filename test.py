from unittest import TestCase
from app import app
from flask import session, request
from boggle import Boggle
import json

app.config["TESTING"] = True

class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!

    def test_home(self):
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn(' <h2>Welcome To Boggle!</h2>', html)

    def test_check_guess(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['board'] = [
                    ['Q', 'P', 'G', 'K', 'A'],
                    ['J', 'E', 'T', 'T', 'E'],
                    ['C', 'S', 'A', 'J', 'M'],
                    ['P', 'L', 'I', 'Z', 'F'],
                    ['M', 'B', 'R', 'V', 'F']
                ]
                change_session['found'] = list()

            res = client.get('/guess?guess=jet')
            self.assertEqual(res.status_code, 200)
            self.assertEqual(json.loads(res.data), {'on_board': 'ok', 'found': False})
      
from unittest import TestCase
from app import app
from flask import session, request
from boggle import Boggle
import json

app.config["TESTING"] = True

class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!

    def test_home(self):
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn(' <h2>Welcome To Boggle!</h2>', html)

    def test_game(self):
        with app.test_client() as client:
            res = client.get('/game')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(session['high_score'], 0)
            self.assertEqual(session['found'], [])
            self.assertIn('<h2> High Score: <i id="high-score">0</i></h2>', html)
            

    def test_check_guess(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['board'] = [
                    ['Q', 'P', 'G', 'K', 'A'],
                    ['J', 'E', 'T', 'T', 'E'],
                    ['C', 'S', 'A', 'J', 'M'],
                    ['P', 'L', 'I', 'Z', 'F'],
                    ['M', 'B', 'R', 'V', 'F']
                ]
                change_session['found'] = ['meat']

            res = client.get('/guess?guess=jet')
            self.assertEqual(res.status_code, 200)
            self.assertEqual(json.loads(res.data), {'on_board': 'ok', 'found': False})

            res = client.get('/guess?guess=meat')
            self.assertEqual(res.status_code, 200)
            self.assertEqual(json.loads(res.data), {'on_board': 'ok', 'found': True})

            res = client.get('/guess?guess=said')
            self.assertEqual(res.status_code, 200)
            self.assertEqual(json.loads(res.data), {'on_board': 'not-on-board', 'found': False})

            res = client.get('/guess?guess=sfefeff')
            self.assertEqual(res.status_code, 200)
            self.assertEqual(json.loads(res.data), {'on_board': 'not-word', 'found': False})
      
    def test_found(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['found'] = []
            res = client.post('/found', data=json.dumps({'guess': 'jet'}))
            
            self.assertEqual(res.status_code, 200)
            self.assertIn('jet', session['found'])

    def test_end_game(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['high_score'] = 0
                change_session['num_plays'] = 0

            res = client.get('/end-game? score= 5')

            self.assertEqual(res.status_code, 200)
            self.assertEqual(session['high_score'], 5)            
            self.assertEqual(session['num_plays'], 1)            
            self.assertEqual(json.loads(res.data), {'high_score': 5, 'num_plays': 1})
            res = client.get('/end-game? score= 3')
            self.assertEqual(session['high_score'], 5)
            self.assertEqual(session['num_plays'], 2)
            
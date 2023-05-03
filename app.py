from flask import Flask, render_template, request, url_for, redirect
from flask_socketio import SocketIO, emit
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hatwati'
socketio = SocketIO(app, logging=True, engineio_logger=True)

user_balances = {'Alina': 0, 
                 'Bhavya': 0, 
                 'Cathy': 0, 
                 'Devu': 0, 
                 'Gautam': 0, 
                 'Gauri': 0, 
                 'Haley': 0, 
                 'Janvi': 0, 
                 'Ketul': 0, 
                 'Kevin': 0, 
                 'Kinolee': 0, 
                 'Nikita': 0, 
                 'Nish': 0, 
                 'Rajiv': 0, 
                 'Rasu': 0, 
                 'Sanay': 0, 
                 'Sanjana': 0, 
                 'Sanya': 0, 
                 'Shreya': 0, 
                 'Sidhi': 0, 
                 'Tanisha': 0, 
                 'Tara': 0, 
                 'Teju': 0}

live_bets = []
example_bet = ("Alina", "Cathy", 5, "for fun")
live_bets.append(example_bet)

def user_one_won(bet):
    loser = bet[1]
    bet_amount = bet[2]
    user_balances[loser] += bet_amount
    # make sure to clear the bet from live bets

def user_two_won(bet):
    loser = bet[0]
    bet_amount = bet[2]
    user_balances[loser] += bet_amount
    # make sure to clear the bet from live bets


@socketio.on('connected')
def connected():
    return "connected"

@socketio.on('send bet')
def add_bet(bet, methods=['GET', 'POST']):
    data = json.loads(bet)
    bet_amount = data['bet_amount']
    user_one = data['user_one']
    user_two = data['user_two']
    bet_description = data['bet_description']

    new_bet = (user_one, user_two, bet_amount, bet_description)
    live_bets.append(new_bet)
    print("bet added" + str(bet_amount) + str(user_one) + str(user_two) + str(bet_description))

# @socketio.on('update live bets')
# def update_live_bets(methods=['GET', 'POST']):
#     emit('update live bets', json.dumps(live_bets))

@app.route('/')
def landing():
    return render_template('landing.html')
    
@app.route('/bop-board', methods=['GET', 'POST'])
def load_bop_board():
    user = request.cookies.get('user')
    if "login" in request.form:
        return render_template('bop-board.html')
    if "bopruptcy" in request.form:
        user_balances[user] = 0
        return render_template('bop-board.html')
    if "add" in request.form:
        user_balances[user] += 1
        return render_template('bop-board.html')
    if "remove" in request.form:
        user_balances[user] -= 1
        return render_template('bop-board.html')
    return render_template('bop-board.html')

@app.route('/live-bets')
def load_live_bets():
    return render_template('live-bets.html')

@app.route('/make-a-bet', methods=['GET', 'POST'])
def load_make_a_bet():
    return render_template('make-a-bet.html')

@app.route('/info')
def load_info():
    return render_template('info.html')

@app.route('/logout')
def load_logout():
    return render_template('logout.html')

if __name__ == '__main__':
    socketio.run(app, debug=True)

# while True:
#     socketio.emit('update live bets', json.dumps(live_bets))
#     socketio.sleep(3)
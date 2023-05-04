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

live_bets = {}
currId = 0

@socketio.on('send bet')
def add_bet(json, methods=['GET', 'POST']):
    global live_bets
    global currId
    live_bets[currId] = json
    temp_list = []
    temp_list.append(currId)
    temp_list.append(json)
    print("appended bet to live_bets")
    socketio.emit('update bets', temp_list)
    print("sent 'update bets' to client")
    currId += 1

@socketio.on('please load bets')
def load_all_live_bets():
    global live_bets
    emit('load bets', live_bets, broadcast=False)

@socketio.on('please load bop balances')
def load_bop_balances():
    global user_balances
    emit('load bop balances', user_balances)

@socketio.on('send my balance')
def send_user_balance(user):
    global user_balances
    target_balance = user_balances[user]
    emit('receive my balance', target_balance)

@socketio.on('just bopped')
def remove_bop(user):
    global user_balances
    target_balance = user_balances[user]
    new_balance = int(target_balance) - 1
    if (new_balance < 0):
        new_balance = 0
    else:
        user_balances[user] = new_balance

@socketio.on('user one won')
def user_one_won(betId, methods=['GET', 'POST']):
    global live_bets
    global user_balances
    target_bet = live_bets[int(betId)]
    loser = target_bet['user_two']
    wager = target_bet['bet_amount']
    currentBal = user_balances[loser]
    newBal = int(currentBal) + int(wager)
    user_balances[loser] = newBal
    del live_bets[int(betId)]
    socketio.emit('force bop board reload')
    socketio.emit('force live bets reload')

@socketio.on('user two won')
def user_two_won(betId, methods=['GET', 'POST']):
    global live_bets
    global user_balances
    target_bet = live_bets[int(betId)]
    loser = target_bet['user_one']
    wager = target_bet['bet_amount']
    currentBal = user_balances[loser]
    newBal = int(currentBal) + int(wager)
    user_balances[loser] = newBal
    del live_bets[int(betId)]
    socketio.emit('force bop board reload')
    socketio.emit('force live bets reload')

@app.route('/')
def landing():
    return render_template('landing.html')
    
@app.route('/bop-board', methods=['GET', 'POST'])
def load_bop_board():
    if "login" in request.form:
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
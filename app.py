from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)

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
    if "submit_bet" in request.form:
        return "Sent bet to server!"
    return render_template('make-a-bet.html')

@app.route('/info')
def load_info():
    return render_template('info.html')

@app.route('/logout')
def load_logout():
    return render_template('logout.html')

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = 'stark_industries_secret_key'  # Session ke liye zaroori hai

# --- ROUTE: HOME PAGE ---
@app.route('/')
def index():
    return render_template('index.html')

# --- GAME 1: ROCK PAPER SCISSORS ---
@app.route('/rps', methods=['GET', 'POST'])
def rps():
    result = None
    user_choice = None
    comp_choice = None
    
    # Mapping for display
    choices = {1: "Rock", 2: "Paper", 3: "Scissors"}
    icons = {1: "fa-hand-rock", 2: "fa-hand-paper", 3: "fa-hand-scissors"}

    if request.method == 'POST':
        # User input HTML button se aayega (1, 2, or 3)
        user_choice = int(request.form.get('choice'))
        comp_choice = random.choice([1, 2, 3])
        
        # Logic from your original code
        if user_choice == comp_choice:
            status = "It's a Tie!"
            color = "yellow"
        elif (user_choice == 1 and comp_choice == 3) or \
             (user_choice == 2 and comp_choice == 1) or \
             (user_choice == 3 and comp_choice == 2):
            status = "You Win!"
            color = "#00ff88" # Green
        else:
            status = "You Lose!"
            color = "#ff4d4d" # Red
            
        result = {
            'status': status,
            'user_txt': choices[user_choice],
            'comp_txt': choices[comp_choice],
            'user_icon': icons[user_choice],
            'comp_icon': icons[comp_choice],
            'color': color
        }

    return render_template('rps.html', result=result)

# --- GAME 2: THE PERFECT GUESS ---
@app.route('/guess', methods=['GET', 'POST'])
def guess():
    msg = None
    color = "white"
    
    # Start New Game (Reset Session)
    if 'target' not in session or request.args.get('action') == 'reset':
        session['target'] = random.randint(1, 100)
        session['attempts'] = 0
        msg = "New Target Locked (1-100). Start guessing!"
        color = "#00a8ff"

    if request.method == 'POST':
        try:
            user_guess = int(request.form.get('guess'))
            session['attempts'] += 1
            target = session['target']

            if user_guess == target:
                msg = f"🎉 CORRECT! Number was {target}. Attempts: {session['attempts']}"
                color = "#00ff88" # Win Green
                # Game khatam hone par target hata do taaki refresh pe naya game aye
                session.pop('target', None) 
            elif user_guess < target:
                msg = "Too Low! Try a larger number."
                color = "#ffcc00" # Warning Yellow
            else:
                msg = "Too High! Try a smaller number."
                color = "#ffcc00"
        except ValueError:
            msg = "Please enter a valid number!"
            color = "red"

    return render_template('guess.html', msg=msg, color=color)

if __name__ == '__main__':
    app.run(debug=True)
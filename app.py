from flask import Flask,render_template,request,session
import random

# to create the flask object
app = Flask(__name__)
app.secret_key = "guess-game-secret"

def runguess(number,guess):
    if guess == number:
        return "Right"
    elif abs(guess-number)<=10:
        return "Hot"
    else:
        return "Cold"
    


# to create the route
@app.route("/")
@app.route("/index",methods = ["GET","POST"])
def index():   
    return render_template("index.html")

@app.route("/set-level",methods=["GET","POST"])
def set_level():
    level = 0
    secret_number = 0
    attempt = 0
    total_range = 0
    if request.method == 'POST':
        level = request.form["level"]
        session["level"] = level
    
    if level == "easy":
        secret_number = random.randrange(1,51)
        attempt = 10
        total_range = 51
    elif level == "medium":
        secret_number = random.randrange(1,101)
        attempt = 7
        total_range = 101
    elif level == "hard":
        secret_number = random.randrange(1,201)
        attempt = 5
        total_range = 201
    
    session["secret_number"] =secret_number
    session["attempt"] = attempt
    session["total_range"] = total_range
    session["game_over"] = False
    return render_template("index.html")

@app.route("/guess-number",methods = ["GET","POST"])
def guess_number():
    guess = 0
    if request.method == "POST":
        guess = int(request.form["input"])
    if session.get("game_over"):
        return render_template("index.html" , result="Game Over! Start a new Game.")
    secret_number = session["secret_number"]
    attempt = session["attempt"]
    result = runguess(secret_number,guess)
    if result == "Right":
        session["game_over"] = True
        message = "You Won!🎉"
    else:
        attempt -= 1
        session["attempt"] = attempt
        
        if attempt == 0:
            session["game_over"] = True
            message = "Game Over! 😢"
        else:
            message = result
    return render_template("index.html",result=message,attempt=attempt)
    

if __name__ == "__main__":
    app.run(debug=True)
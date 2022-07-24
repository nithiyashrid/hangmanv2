from flask import Flask, render_template, request,jsonify,session
from flask_session import Session
import hangman

app = Flask(__name__)
app.config["SESSION_PERMANENT"]=False
app.config["SESSION_TYPE"]="filesystem"
Session(app)
hangman_images= ["1.jpg","2.jpg","3.jpg","4.jpg","5.jpg","6.jpg","7.jpg","8.jpg"]

@app.get('/')
def index():
    if not session:    
        word=hangman.startgame()
        length = len(word)
        notGuessed = '_ '*length
        forhtml ="&lowbar;&nbsp;"*length
        print(notGuessed)
        print(word)
        session["word"]=word
        session["length"]=length
        session["guessed"]=set()
        session["notGuessed"]=notGuessed
        session["wrongGuess"]=0
        session["wordSet"]=set(word)
    else:
        notGuessed = session["notGuessed"]
    url = "https://raw.githubusercontent.com/nithiyashrid/hangmanImages/main/" + hangman_images[session["wrongGuess"]]
    print(type(session['notGuessed']),session['notGuessed'])
    return render_template('index.html',notGuessed=notGuessed,url=url)


@app.post('/')
def check():
    data = request.json
    if data['type']=="check":
        nextChar = data['input']
        result = hangman.check(nextChar,session['word'],session['guessed'])
        print(result[1])
        if result[0]=="correct":
            session["guessed"].add(nextChar)
            session['notGuessed']=result[1]
            output = session['notGuessed']
            if session["guessed"]==session["wordSet"]:
                print("You win")
                return jsonify({'type':'win','foundWord':"You win"})
            else:
                return jsonify({ 'type':'correct','foundWord':output})
        elif result[0]=="wrong":
            session["wrongGuess"] += 1
            url = "https://raw.githubusercontent.com/nithiyashrid/hangmanImages/main/" + hangman_images[session["wrongGuess"]]
            output = "Wrong guess :( - No. of Attempts left : "+ str(8-session["wrongGuess"]) 
            return jsonify({'type':'wrong','foundWord':output,'url':url})
        else:
            output = "Cannot guess the same letter again, change your guess"
            return jsonify({'type':'same','foundWord':output})

if __name__ == '__main__':
    app.run(debug=True)
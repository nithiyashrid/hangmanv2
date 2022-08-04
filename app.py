from logging import exception
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
    if not session or session["wrongGuess"] >= 7:    
        word=hangman.startgame()
        length = len(word)
        notGuessed = '_ '*length
        print(word)
        session["word"]=word
        session["length"]=length
        session["guessed"]=set()
        session["notGuessed"]=notGuessed
        session["wrongGuess"]=0
        session["wordSet"]=set(word)
        session["gameover"]=False
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
        print(nextChar)
        result = hangman.check(nextChar,session['word'],session['guessed'],session['wrongGuess'])

        if result[0]=="gameover":
            return jsonify({'type':'gameover','correctWord':session['word']})

        if result[0]=="correct":
            session["guessed"].add(nextChar)
            session['notGuessed']=result[1]
            output = session['notGuessed']
            if session["guessed"]==session["wordSet"]:
                session["gameover"]=True
                print("You win")
                return jsonify({'type':'win','foundWord':session['word']})
            else:
                return jsonify({ 'type':'correct','foundWord':output})
        elif result[0]=="wrong":
            session["wrongGuess"] += 1
            url = "https://raw.githubusercontent.com/nithiyashrid/hangmanImages/main/" + hangman_images[session["wrongGuess"]]
            output = 7-session["wrongGuess"]
            print(output)
            if output>0:
                return jsonify({'type':'wrong','attempts':str(output),'url':url})
            else:
                return jsonify({'type':'gameover','correctWord':session['word'],'url':url})
        elif result[0]=="noinput":
            print(result[1])
            return jsonify({'type':'same','foundWord':result[1]})
        else:
            return jsonify({'type':'same','foundWord':result[1]})

    if data['type']=='newgame':
        word=hangman.startgame()
        length = len(word)
        notGuessed = '_ '*length
        print(word)
        session["word"]=word
        session["length"]=length
        session["guessed"]=set()
        session["notGuessed"]=notGuessed
        session["wrongGuess"]=0
        session["wordSet"]=set(word)
        session["gameover"]=False
        url = "https://raw.githubusercontent.com/nithiyashrid/hangmanImages/main/" + hangman_images[session["wrongGuess"]]
        print(type(session['notGuessed']),session['notGuessed'])
        return render_template('index.html',notGuessed=session["notGuessed"],url=url)

if __name__ == '__main__':
    app.run(debug=True)
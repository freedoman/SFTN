from flask import Flask, url_for, redirect, session, request

app = Flask(__name__)

@app.route("/evernote_callback")
def evernote_callback():
    print(request.args)
    return "Ok"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8888)
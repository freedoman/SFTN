from flask import Flask, url_for, redirect, session, request
import evernote.edam.type.ttypes as Types
from evernote.api.client import EvernoteClient
from ImportToNote import ImportToNote

EN_CONSUMER_KEY = ""
EN_CONSUMER_SECRET = ""
SECRET_KEY = "everything is ok"

app = Flask(__name__)
app.config.from_object(__name__)

@app.route("/")
def index():
    authorize_url = auth()
    return redirect(authorize_url)

@app.route("/evernote_callback")
def evernote_callback():
    session["oauth_verifier"] = request.args.get("oauth_verifier", "")
    get_access_token()
    ImportToNote(session["access_token"])
    return "Data is tranfering to Evernote!"

def get_evernote_client(token=None):
    if token:
        return EvernoteClient(token=token, sandbox=True)
    else:
        return EvernoteClient(consumer_key=EN_CONSUMER_KEY, consumer_secret=EN_CONSUMER_SECRET,sandbox=True)

def auth():
    print("auth start")
    callback = "http://localhost:8888/evernote_callback"
    client = get_evernote_client()
    req_token = client.get_request_token(callback)
    print(req_token)
    session["oauth_token"] = req_token["oauth_token"]
    session["oauth_token_secret"] = req_token["oauth_token_secret"]
    return client.get_authorize_url(req_token)

def get_access_token():
    try:
        client = get_evernote_client()
        session["access_token"] = client.get_access_token(session['oauth_token'], session['oauth_token_secret'],session['oauth_verifier'])
    except KeyError:
        print("KeyError")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8888, debug = "enable")











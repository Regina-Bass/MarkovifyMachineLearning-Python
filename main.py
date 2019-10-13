from flask import Flask, render_template
from flask_socketio import SocketIO
from twitter_scraper_fetcher import *
from mlh_twitter_api import moderate
import json
import config
import random
from markov import *        #usually this is bad practice because of merge clashes (method with same names for example) and even if it works you may not know the library/code very well

app = Flask(__name__)
socketio = SocketIO(app)

# Renders UI
@app.route("/")
def home():
  return render_template("homepage.html")

# Chat API - WebSocket
@socketio.on("send question")
def generate_message(body, methods=["POST"]):
  user_question = body["message"]
  twitter_handle = body["username"]

  # Call get_user_tweets() from twitter_scraper_fetcher.py to scrape some tweets
  tweets = get_user_tweets(twitter_handle)
  try:
    cleaned_tweets = clean_tweets_data(tweets)
    # Get a random tweet from the list of tweets
    bot_answer = generate_bot_answer(twitter_handle, user_question)
    print(bot_answer)
    #moderated_answer = moderate(bot_answer)
    #print("Hello ", moderated_answer)
    # Send the answer to the app, to display to the user
    answer = {"username": twitter_handle, "message": bot_answer}
    print(answer)
    socketio.emit("bot answer", answer)
  except:
    bot_answer = "Sorry, I couldn't process that. Try again please."
    socketio.emit("error", {"username": twitter_handle, "message": bot_answer})

if __name__ == "__main__":
    socketio.run(app)


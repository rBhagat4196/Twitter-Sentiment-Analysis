import re 
from textblob import TextBlob 
from textblob.sentiments import NaiveBayesAnalyzer
from flask import Flask, render_template , redirect, url_for, request ,jsonify
import requests



def clean_tweet( tweet): 
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split()) 
         
def get_tweet_sentiment( tweet): 
        analysis = TextBlob(clean_tweet(tweet)) 
        if analysis.sentiment.polarity > 0:
            return "positive"
        elif analysis.sentiment.polarity == 0:
            return "neutral"
        else:
            return "negative"


def get_tweets(query, count=5): 
        # Construct the URL for your Express.js API
        tweets = [] 
        fetched_tweets = []
        api_url = f'http://localhost:4000/tweet/{query}/{count}'
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            fetched_tweets = data
        
        for tweet in fetched_tweets: 
            parsed_tweet = {} 

            parsed_tweet['text'] = tweet
            parsed_tweet['sentiment'] = get_tweet_sentiment(parsed_tweet['text']) 
                        
            tweets.append(parsed_tweet) 
        return tweets 

        

app = Flask(__name__)
app.static_folder = 'static'

@app.route('/')
def home():
  return render_template("index.html")

# ******Phrase level sentiment analysis
@app.route("/predict", methods=['POST','GET'])
def pred():
	if request.method=='POST':
            query=request.form['query']
            count=request.form['num']
            fetched_tweets = get_tweets(query, count) 
            return render_template('result.html', result=fetched_tweets)

# fetched_tweets
# [
#   {"text" : "tweet1", "sentiment" : "sentiment1"},
#   {"text" : "tweet2", "sentiment" : "sentiment2"},
#   {"text" : "tweet3", "sentiment" : "sentiment3"}
# ]

# *******Sentence level sentiment analysis
@app.route("/predict1", methods=['POST','GET'])
def pred1():
	if request.method=='POST':
            text = request.form['txt']
            blob = TextBlob(text)
            if blob.sentiment.polarity > 0:
                text_sentiment = "positive"
            elif blob.sentiment.polarity == 0:
                text_sentiment = "neutral"
            else:
                text_sentiment = "negative"
            return render_template('result1.html',msg=text, result=text_sentiment)


if __name__ == '__main__':
    app.debug=True
    app.run(host='localhost')

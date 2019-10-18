import twitter  # import the Twitter library
import config  # import contents of .config
from flask import Flask

app = Flask(__name__)  # Initialize a new Flask object


@app.route('/')
def home():
    return "<h1> Hello World </h1>"


if __name__ == "__main__":
    app.run(debug=True, port=8080)


file = open("tweets.txt", "w+")

# initialize api instance (build a Twitter.api object)
twitter_api = twitter.Api(consumer_key=config.ACCESS_TOKEN,
                          consumer_secret=config.ACCESS_SECRET,
                          access_token_key=config.CONSUMER_KEY,
                          access_token_secret=config.CONSUMER_SECRET)


def collectTweets(keyword):  # function to collect tweets with a specified keyword
    try:  # testing this block of code for errors
        tweets_fetched = twitter_api.GetSearch(keyword, count=10)  # collect first 25 tweets with the keyword

        # print("Fetched " + str(len(tweets_fetched)) + " tweets for the term " + keyword)

        tweet_info = [
            {"Tweet": status.text,
             "Create Date": status.created_at,
             "URL": status.urls,
             "label": None}
            for status in tweets_fetched]

        return tweet_info
        # print the text and label (placeholder for polarity) for each tweet recovered

    except:  # if an error persists, run this
        print("Unfortunately, there was an error. Try again!")
        return None


search_term = input("Enter a search keyword:")
testDataSet = collectTweets(search_term)  # saves the tweets as a dictionary

# Print to a .txt file
with open('tweets.txt', 'w+') as f:
    for key in testDataSet:
        print(key, file=f)
        print("\n" + " \n")

file.close()




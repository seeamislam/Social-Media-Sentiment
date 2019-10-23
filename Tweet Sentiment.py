import twitter  # import the Twitter library
import config  # import contents of .config
import re  # Regular expression library - Helps us parse strings and modify them in efficient ways
from nltk.tokenize import word_tokenize  # NLP toolkit library
from string import punctuation
from nltk.corpus import stopwords

file = open("tweets.txt", "w+")

# initialize api instance (build a Twitter.api object)
twitter_api = twitter.Api(consumer_key=config.ACCESS_TOKEN,
                          consumer_secret=config.ACCESS_SECRET,
                          access_token_key=config.CONSUMER_KEY,
                          access_token_secret=config.CONSUMER_SECRET)


def collectTweets(keyword):  # function to collect tweets with a specified keyword
    tweets_fetched = twitter_api.GetSearch(keyword, count=10)  # collect first 25 tweets with the keyword

    # print("Fetched " + str(len(tweets_fetched)) + " tweets for the term " + keyword)

    tweet_info = [{
        "Tweet": status.text,
        "Create Date": status.created_at,
        "URL": status.urls,
        "label": None}
        for status in tweets_fetched]

    return tweet_info


search_term = input("Enter a search keyword:")
testDataSet = collectTweets(search_term)  # saves the tweets as a dictionary

# Print to a .txt file
with open('tweets.txt', 'w+') as f:
    for key in testDataSet:
        print(key, file=f)
        print("\n" + " \n")

file.close()


# To train our data set, we will use Niek Sander's Corpus of already classified tweets
# FUN FACT: Corpus means large and structured set of text.
# Twitter does not let us save tweets on a device, so we first have to fetch them.
# Corpus contains the topic, label (pos/neg) and ID of each tweet, so we can fetch it and store it.


def buildTrainingSet(corpusFile, tweetDataFile):  # corpusFile will contain the attributes of each tweet we need
    import csv
    import time

    rawTweets = []  # Empty list which will hold tweet id, labels, and topics.

    with open(corpusFile, 'r') as csvfile:  # open corpusFile
        lineReader = csv.reader(csvfile, delimiter=',', quotechar="\"")
        for row in lineReader:
            rawTweets.append({"tweet_id": row[2], "label": row[1], "topic": row[0]})
            #  Using this, we append every tweet in the file to our list

    rate_limit = 180
    sleep_time = 900 / rate_limit
    # 900 seconds = 15 mins, which is the time window between requesting another set of 180 tweets
    # Our goal is to download 5000 hand-classified tweets, so building our data set will take some time.

    trainingDataSet = []  # empty list to store tweets

    for tweet in rawTweets:  # Now, we will loop through each tweet in our list of raw tweets
        try:
            status = twitter_api.GetStatus(tweet["tweet_id"])
            # Call the API on every tweetID in the list and get its status (status contains the raw text of the tweet)
            print("Tweet fetched" + status.text)
            tweet["text"] = status.text
            trainingDataSet.append(tweet)  # append the raw text of the tweet to our new csv training set
            time.sleep(sleep_time)  # we have to wait 15 minutes as per restrictions by the API
        except:
            continue

    # now we write them to the empty CSV file
    with open(tweetDataFile, 'w') as csvfile:
        linewriter = csv.writer(csvfile, delimiter=',', quotechar="\"")
        for tweet in trainingDataSet:
            try:
                linewriter.writerow([tweet["tweet_id"], tweet["text"], tweet["label"], tweet["topic"]])
            except Exception as e:  # This allows us to still access attributes of the object
                print(e)
    return trainingDataSet


corpusFile = "/Users/orange/py-ground/Twitter-Sentiment/corpus.csv"
tweetDataFile = "/Users/orange/py-ground/Twitter-Sentiment/tweetDataFile.csv"

# trainingData = buildTrainingSet(corpusFile, tweetDataFile)  # Used to build the training data
trainingData = "/Users/orange/py-ground/Twitter-Sentiment/tweetDataFile.csv"


class PreProcessTweets:
    def __init__(self):
        self._stopwords = set(stopwords.words('english') + list(punctuation) + ['AT_USER', 'URL'])
        #  The constructor of this class removes STOP words
        #  Stop words are useless words that should be removed during preprocessing - such as the, a, an
        #  Fortunately, we can use a function in NLTK to remove them

    def tokenizeTweets(self, tweet):
        #  Process the tweets to lower case, remove URLS, usernames, hashtags, and remove repeated characters
        #  We will use the re (regular expression) library to manipulate our strings
        tweet = tweet.lower()  # to lower-case
        tweet = re.sub('((https?://[^\s]+)|(www\.[^\s]+))', 'URL', tweet)  # remove URLs
        tweet = re.sub('@[^\s]+', 'AT_USER', tweet)  # remove usernames
        tweet = re.sub(r'#([^\s]+)', r'\1', tweet)  # remove the # in #hashtag
        tweet = word_tokenize(tweet)  # remove repeated characters
        return [word for word in tweet if word not in self._stopwords]

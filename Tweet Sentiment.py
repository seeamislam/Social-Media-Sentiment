import twitter  # import the Twitter library
import config  # import contents of .config

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


def buildTrainingSet(corpusFile, tweetDataFile):  # corpusFile will contain the downloaded training set
    import csv
    import time

    rawTweets = []  # Empty list which we will append the tweets from corpusFile to

    with open(corpusFile, 'rb') as csvfile:  # open corpusFile
        lineReader = csv.reader(csvfile, delimiter=',', quotechar="\"")
        for row in lineReader:
            rawTweets.append({"tweet_id": row[2], "label": row[1], "topic": row[0]})
            #  Using this, we append every tweet in the file to our list of tweets

    rate_limit = 180
    sleep_time = 900 / 180

    trainingDataSet = []  # empty list to store tweets

    for tweet in rawTweets:  # Now, we will loop through each tweet in our list of raw tweets
        try:
            status = twitter_api.GetStatus(tweet["tweet_id"])
            # Call the API on every tweet in the list and get its status (status contains the raw text of the tweet)
            print("Tweet fetched" + status.text)
            tweet["text"] = status.text
            trainingDataSet.append(tweet)  # append the raw text of the tweet to our new csv training set
            time.sleep(sleep_time)  # we have to wait 5 minutes as per restrictions by the API
        except:
            continue


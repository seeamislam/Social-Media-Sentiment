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


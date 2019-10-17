import twitter  # import the Twitter library
import config  # import contents of .config

# initialize api instance (build a Twitter.api object)
twitter_api = twitter.Api(consumer_key=config.ACCESS_TOKEN,
                          consumer_secret=config.ACCESS_SECRET,
                          access_token_key=config.CONSUMER_KEY,
                          access_token_secret=config.CONSUMER_SECRET)

# test authentication
print(twitter_api.VerifyCredentials())





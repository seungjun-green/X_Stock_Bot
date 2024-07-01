import tweepy

consumer_key = 'mrpnK8usre8ahxxVIFs9SpGQf'
consumer_secret = '2hMFSVggEsEKG3dL4sepdMw56XZ6U0R2uG04ej0lTB9MZBjSCO'
access_token = '1805518108750495748-dou33BfVJCpGfVSN6iNOXFUbCmRZSR'
access_token_secret = 'c2zC39MgG4Zxb9rItzSrH75DHwSJJJu0mT1Rmc4cpz6Lk'

client = tweepy.Client(
    consumer_key=consumer_key, 
    consumer_secret=consumer_secret,
    access_token=access_token, 
    access_token_secret=access_token_secret
)

# Create the API object
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

        
def make_tweet(txt, image_path):
    media = api.media_upload(filename=image_path)
    
    response = client.create_tweet(
        text=txt,
        media_ids=[media.media_id]
    )
    return response



def make_tweet_text(tweet_string):
    client.create_tweet(text=tweet_string)
    
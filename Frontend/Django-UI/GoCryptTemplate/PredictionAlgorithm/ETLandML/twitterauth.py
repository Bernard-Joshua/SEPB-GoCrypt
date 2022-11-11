# Import the Python Library for Twitter-API.
import tweepy

# Get the authentication keys:
api_key = "UQazeKSxbwRnLXlDJiie8NBSD"
api_secret = "uziW5pJKvxSVPSCReOp2XiLsv5M37BjfumgOQhKxkbCiejXGB2"
access_token = "1456438378581278721-t5SpZ7a3z5kdwdLjoNf9z97HI7Jfhd"
access_token_secret = "jrMt0chMwXTJHF4bdWdZIlRSyCO1gPsZgGU8vUS0eWh1c"
bearer_token = "AAAAAAAAAAAAAAAAAAAAAPM6ggEAAAAAa6w8pf%2FEj1nw8KnjgnxWEv%2FCNmU%3DOGgWYZexPgkv2wvMTKiGC3tG4xAL4Uy6mQuIqyBXMDxgmQ91Ov"

# Connecting to Twitter API using Credentials
client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)

# Authenticating Developer Credentials
auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
api = tweepy.API(auth)


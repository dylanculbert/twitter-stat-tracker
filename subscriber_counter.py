import tweepy
import pygsheets
import datetime

api_bearer_token = 'replace'
twitter_handle = 'replace'
google_sheet_name = 'replace'

def get_follower_and_tweet_count(user):
    client = tweepy.Client(api_bearer_token)
    user = client.get_user(username=user, user_fields=['public_metrics'])
    return user.data['public_metrics']['followers_count'], user.data['public_metrics']['tweet_count']

def append_twitter_data_to_google_sheet(follower_number, tweet_number):
    g_client = pygsheets.authorize(service_file='google_sheets_key.json')
    spread_sheet = g_client.open(google_sheet_name)
    date = str(datetime.datetime.now())
    work_sheet = spread_sheet.sheet1
    work_sheet.append_table(values=[date, follower_number, tweet_number])

def twitter_data_handler(event, context):
    follower_number, tweet_number = get_follower_and_tweet_count(twitter_handle)
    append_twitter_data_to_google_sheet(follower_number, tweet_number)
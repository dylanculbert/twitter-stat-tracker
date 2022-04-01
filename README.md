## Overview

This is a quick and dirty python to track your twitter followers.

I plan to improve upon this readme at some point as well as making it deployable with sam and cloudformation.

## Prerequisites

1) Sign up to get [twitter api access](https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api) and take note of your **Bearer Token**
2) Create a [google service account] (https://cloud.google.com/iam/docs/creating-managing-service-account-keys) and obtain the **credentials.json** file, make sure the service account has access to the google sheets api.
3) Create a google sheet and take note of the **name**, share the file with write access to the email for the service account in the previous step.
4) Set `api_bearer_token` in `subscriber_counter.py` to the **Bearer Token** from step 1.
5) Set `twitter_handle` in `subscriber_counter.py` the twitter handle you wish to track stats for.
6) Set `google_sheet_name` to the name of the spreadsheet you created in step 3.
5) Replace the contents of `google_sheets_key.json` with the contents of the **credentials.json** from google service account created in step 2.
6) Ensure you have python installed (I used 3.8)
7) Create a virtual environment by running `python3 -m venv ./venv` from the root of this project.
8) Activate your virtual environment by running `source venv/bin/activate`
9) Install dependancies by running `python3 -m pip install -r requirements.txt` 

You can test the that the above worked by running the following locally

```
    follower_number, tweet_number = get_follower_and_tweet_count(twitter_handle)
    append_twitter_data_to_google_sheet(follower_number, tweet_number)
```

## Deployment (Sam should make this less painful)
 
1) Create a folder called `deploy` and copy the contents of `./venv/lib/python3.8/site-packages` to it.
2) Copy `./subscriber_counter.py` to the root of the `deploy` folder.
3) Zip the `deploy` folder to create `deploy.zip`
4) Create a new lambda function with the following:
    - Role: Default lambda role should be enough
    - Handler: subscriber_counter.twitter_data_handler
    - Runtime: Python 3.8
    - Architecture: x86_64
    - Timeout: 1 minute (less should work too)
5) Create a trigger for the lambda using **Add Trigger**
    - Type: EventBridge
    - Click create rule, any name and discription will do
    - Under scheduled expression you can either give it a `rate()` or `cron()` expression, I'm using `cron(0 0 * * ? *)` to run every day at midnight.
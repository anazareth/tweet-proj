import tweepy
import pandas as pd
import numpy as np


def main():
    consumer_key, consumer_secret, access_token, access_secret = get_tokens()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)
    target_username = 'JustinTrudeau'
    out_file = 'out//trudeau_raw.csv'
    # NOTE: tweet id (incrementing) is found in tweet url, advanced search is helpful for looking back
    start_id = 1212375795538309120  # tweet id at least start_id
    final_id = 1256030193325662208  # tweet id at most final_id
    new_tweets = api.user_timeline(screen_name=target_username, since_id=start_id, max_id=final_id, count=1)
    tweets = new_tweets
    final_id = tweets[-1].id - 1  # update final_id to be less than the oldest tweet collected (last in list)
    while len(new_tweets) > 0:  # until we have retrieved all tweets
        # return all tweets in range, 100 at a time
        new_tweets = api.user_timeline(screen_name=target_username, since_id=start_id, max_id=final_id, count=100)
        tweets.extend(new_tweets)
        final_id = tweets[-1].id - 1
        print('...'+str(len(tweets))+' tweets downloaded thus far, up to ' + str(tweets[-1].created_at))
    print(" Downloaded " + str(len(tweets)) + " tweets from " + target_username + ".")

    data_temp = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=["Tweets"])
    data_temp['Length'] = np.array([len(tweet.text) for tweet in tweets])
    data_temp['Date'] = np.array([tweet.created_at for tweet in tweets])
    data_temp['Source'] = np.array([tweet.source for tweet in tweets])
    data_temp['Favourites'] = np.array([tweet.favorite_count for tweet in tweets])
    data_temp['RTs'] = np.array([tweet.retweet_count for tweet in tweets])

    data_temp.to_csv(out_file, index=False, encoding='utf-8')

def get_tokens():
    # TODO: read shhh.txt file containing tokens
    print(consumer_key)
    print(consumer_secret)
    print(access_token)
    print(access_secret)
    return consumer_key, consumer_secret, access_token, access_secret

if __name__ == '__main__':
    get_tokens()


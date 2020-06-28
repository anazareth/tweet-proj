import tweepy
import pandas as pd
import numpy as np
import sys
import datetime as dt

# run script from cmd line like this:
# scraper.py username start_id end_id
# --username (string) - target twitter handle
# --start_id (int) - tweet id (found in URL) of earliest tweet desired
# --end_id (int) - tweet id (found in URL) of final tweet desired


def main():
    consumer_key, consumer_secret, access_token, access_secret = get_tokens()
    # init connection with authentication parameters
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)
    # define user we want to get tweets from
    target_username = sys.argv[1]
    out_file = 'data//'+target_username+'_raw.csv'
    # NOTE: tweet id (incrementing) is found in tweet url, advanced search is helpful for looking back
    start_id = sys.argv[2]  # tweet id at least start_id
    final_id = sys.argv[3]  # tweet id at most final_id
    new_tweets = api.user_timeline(screen_name=target_username, since_id=start_id, max_id=final_id, count=1,
                                   tweet_mode='extended')
    tweets = new_tweets
    final_id = tweets[-1].id - 1  # update final_id to be less than the oldest tweet collected (last in list)

    while len(new_tweets) > 0:  # until we have retrieved all tweets
        # return all tweets in range, 100 at a time
        new_tweets = api.user_timeline(screen_name=target_username, since_id=start_id, max_id=final_id, count=100,
                                       tweet_mode='extended')
        tweets.extend(new_tweets)
        final_id = tweets[-1].id - 1
        print(dt.datetime.today().strftime('%b-%d-%Y %H:%M:%S EST - ') +
              str(len(tweets)) + ' tweets downloaded thus far, up to ' + str(tweets[-1].created_at))
        # time.sleep(6)
    print(dt.datetime.today().strftime('%b-%d-%Y %H:%M:%S EST - ') +
          'Downloaded ' + str(len(tweets)) + ' tweets from ' + target_username + '.')

    data_temp = pd.DataFrame(data=[tweet.full_text for tweet in tweets], columns=["Tweets"])
    data_temp['Length'] = np.array([len(tweet.full_text) for tweet in tweets])
    data_temp['Date'] = np.array([tweet.created_at for tweet in tweets])
    data_temp['Source'] = np.array([tweet.source for tweet in tweets])
    data_temp['Favourites'] = np.array([tweet.favorite_count for tweet in tweets])
    data_temp['RTs'] = np.array([tweet.retweet_count for tweet in tweets])
    data_temp['Username'] = target_username
    data_temp['id_str'] = np.array([tweet.id for tweet in tweets])

    data_temp.to_csv(out_file, index=False, encoding='utf-8')


def get_tokens():
    f = open('shhh.txt', 'r')
    f.readline()
    consumer_key = f.readline().rstrip("\n")
    consumer_secret = f.readline().rstrip("\n")
    access_token = f.readline().rstrip("\n")
    access_secret = f.readline()
    f.close()
    return consumer_key, consumer_secret, access_token, access_secret


if __name__ == '__main__':
    print(dt.datetime.today().strftime('%b-%d-%Y %H:%M:%S EST - ') +
          'STARTING program ' + sys.argv[0] + '...')
    main()


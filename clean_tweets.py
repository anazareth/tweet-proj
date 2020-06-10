import pandas as pd
from langdetect import detect, lang_detect_exception
import numpy as np
import datetime as dt
import os
import sys

# run from cmd line like so:
# clean_tweets.py data//trudeau_raw.csv

input_csv = sys.argv[1]
remove_rts = True if sys.argv[2] == 1 else False
output_name = input_csv.replace('raw', 'clean')
default_lang = 'en'


def main():

    df = pd.read_csv(input_csv)  # read csv containing output of twitter scraper

    df = format_cols(df)
    add_data(df)  # append new tweets to database


def format_cols(df):
    num_tweets_read = df.shape[0]  # number of tweets ingested
    print(dt.datetime.today().strftime('%b-%d-%Y %H:%M:%S EST - ') +
          str(num_tweets_read) + ' tweets read from file \'' + input_csv + '\'.')  # log message

    # -- remove retweets --
    df['isRT'] = df.copy()['Tweets'].str.startswith('RT')  # label RTs (true/false)

    if remove_rts:
        df = df.loc[df['isRT'] is False].copy()  # keep only non-retweets

    num_rts = num_tweets_read - df.shape[0]  # (number of tweets read) - (number remaining after removing RTs)
    print(dt.datetime.today().strftime('%b-%d-%Y %H:%M:%S EST - ') +
          str(num_rts) + ' RTs removed.')  # log message

    # -- remove media links and tweets only containing these links --
    df['tco'] = df['Tweets'].str.replace('(https:\/\/t\.co\/[-a-zA-Z0-9]{1,256})')
    df['Tweets'] = df['Tweets'].copy().str.replace('https:\/\/t\.co\/[-a-zA-Z0-9]{1,256}', '')
    df['Tweets'] = df['Tweets'].str.strip()

    # -- remove french tweets --
    # use langdetect package to create column specifying language
    df['Language'] = np.array([my_detect(t) for t in df['Tweets']])

    num_french_tweets = df.loc[(df['Language'] == 'fr')].shape[0]  # number of french tweets detected
    # keep non-french tweets (any other language classification is almost certainly incorrect)
    df = df.loc[(df['Language'] != 'fr')].copy()
    print(dt.datetime.today().strftime('%b-%d-%Y %H:%M:%S EST - ') +
          str(num_french_tweets) + ' French tweets removed.')  # log message
    # -- create month column --
    df['Date'] = pd.to_datetime(df['Date'])  # set date type
    df['Month'] = df['Date'].dt.month_name()  # create column month name from date

    return df


def add_data(df):
    if os.path.exists(output_name):  # if there is existing data
        main_data = pd.read_csv(output_name, encoding='utf-8')  # read csv of existing data
        num_rows_main = main_data.shape[0]  # number of rows in the main dataset before adding to it
        updated_df = pd.concat([main_data, df], sort=False)  # update data by appending new tweets
        updated_df.reset_index(drop=True)
    else:
        num_rows_main = 0
        print(dt.datetime.today().strftime('%b-%d-%Y %H:%M:%S EST - ') +
              'Adding data for the first time to data/' + output_name)  # log message
        num_new_rows = df.shape[0]
        updated_df = df

    temp_num_rows = updated_df.shape[0]  # to calculate how many rows we drop in the next line
    updated_df.drop_duplicates(subset=['id_str'], keep='first',
                               inplace=True)  # drop duplicates in case old tweets were downloaded mistakenly
    num_rows_updated = updated_df.shape[0]  # number of rows in the updated main dataset
    num_rows_dropped = temp_num_rows - num_rows_updated
    print(dt.datetime.today().strftime('%b-%d-%Y %H:%M:%S EST - ') +
          str(num_rows_dropped) + ' rows dropped.')
    num_new_rows = num_rows_updated - num_rows_main  # number of rows added to the main dataset

    print(dt.datetime.today().strftime('%b-%d-%Y %H:%M:%S EST') + ' - ' +
          str(num_new_rows) + ' new rows saved to ' + output_name)
    updated_df.to_csv(output_name, encoding='utf-8', index=False)  # save updated data as csv

    # if os.path.exists(input_csv):
    #     source_path = input_csv
    #     target_path = os.path.join('old', input_csv)
    #     os.rename(source_path, target_path)  # move the input data file since we don't need it anymore


def my_detect(text):
    # handle exception thrown by
    try:
        return detect(text)
    except lang_detect_exception.LangDetectException:
        print(dt.datetime.today().strftime('%b-%d-%Y %H:%M:%S EST - ') +
              'default lang (' + default_lang + ') set for tweet: ' + text )
        return default_lang


if __name__ == '__main__':
    main()

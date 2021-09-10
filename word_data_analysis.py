'''
Short Description: Get some metrics about keyword frequency by Twitter user and month, especially relating to COVID-19
'''

__author__ = 'Alex Nazareth' 

import os
from numpy.lib.function_base import cov
import pandas as pd
from ast import literal_eval
from collections import Counter

YEAR = 2020

# words_df cols: ['Tweets', 'Length', 'Date', 'Source', 'Favourites', 'RTs', 'Username', 'id_str', 'isRT', 'tco', 'Language', 'Month', 'TweetsTokenized']
def main(words_df, out_filename, username):
    # month_range = ['MarToJun', 'March', 'April', 'May', 'June']:
    month_range = ['Y2020', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
                   'September', 'October', 'November', 'December']
    col_names = ['username', 'year', 'month', 'num_covid_mentions',
                 'num_words_total', 'num_covid_tweets', 'total_num_tweets']
    df_month_words = words_df[words_df['Month'].isin(month_range)]
    new_df = pd.DataFrame(columns=col_names)
    for mth in month_range:
        if mth != 'Y2020':
            df_month_words =  words_df[words_df['Month'] == mth]
        covid_freq, all_kw_freq, num_covid_tweets, num_total_tweets = get_metrics(df_month_words)
        num_covid_mentions, num_keywords, = sum(covid_freq), sum(all_kw_freq)
        print('Covid was mentioned', num_covid_mentions, 'times by @' + username,'in', mth, 'out of', num_keywords, 'word mentions.')
        print('It was also mentioned in', num_covid_tweets, 'tweets out of', num_total_tweets, 'that month.')
        print('--')
        new_row = pd.DataFrame(data=[[username, YEAR, mth, num_covid_mentions, num_keywords, num_covid_tweets, num_total_tweets]], columns=col_names)
        new_df = new_df.append(new_row, ignore_index=True)
    if os.path.exists(out_filename):  # append to existing data
        existing_df = pd.read_csv(out_filename)
        updated_df = existing_df.append(new_df, ignore_index=True)
    else:
        updated_df = new_df
    updated_df.to_csv(out_filename, index=False)


def get_metrics(df_mw):
    # input pd.DataFrame has columns 'Month' and 'TweetsTokenized', the latter a string literal of a list of keywords from the tweet
    covid_keywords = ['covid', 'covid19', 'coronavirus', 'virus', 'pandemic']

    # wordlistlist = [wlist for strwlist in df_mw['TweetsTokenized'] for wlist in literal_eval(strwlist)]
    wordlistlist = [literal_eval(strwlist) for strwlist in df_mw['TweetsTokenized']]

    num_covid_tweets = len([1 for wl in wordlistlist if bool(set(wl).intersection(covid_keywords))])
    num_total_tweets = len(wordlistlist)

    # df_mw['covid_tweet'] = len([w for tweet in df_mw['TweetsTokenized'] for w in literal_eval(tweet) if w in covid_keywords]) > 0
    
    all_keywords = [w for wlst in df_mw['TweetsTokenized'] for w in literal_eval(wlst)]  # evaluate literal and combine all words into one list
    word_freq = pd.Series(Counter(all_keywords)).sort_values(ascending=False)
    covid_word_freq = word_freq[word_freq.index.isin(covid_keywords)]
    return covid_word_freq, word_freq, num_covid_tweets, num_total_tweets


if __name__=='__main__':
    #  original, before Linda
    # out_filename = 'data\\covid\\monthly_covid_mentions.csv'  # append all data to this file
    # search_dir = 'data\\kw_ana'
    out_filename = 'data\\covid\\monthly_covid_mentions_v2.csv'  # append all data to this file
    search_dir = 'data\\kw_ana\\linda_govs'
    for fname in os.listdir(search_dir):  # full year of governor data from Linda
        if fname.endswith('_tokenized.csv') and 'sample' not in fname.lower():
            username =  '_'.join(fname.split('_')[:-1])
            in_filename = search_dir + '\\' + fname
            in_df = pd.read_csv(in_filename)
            main(in_df, out_filename, username)
    # username = 'realDonaldTrump'
    # in_df = pd.read_csv(in_filename)
    # main(in_df, out_filename, username)
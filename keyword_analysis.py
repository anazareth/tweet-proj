import pandas as pd
import numpy as np
import sys
import os
from nltk.corpus import stopwords
import regex
from ast import literal_eval
import datetime as dt

# keyword_analysis.py data//trudeau_clean.csv ism_txt stopwords_txt username
# --input_csv (str) - name of csv file (and path if necessary)
# --stopwords_txt (str) - text file with list of extra stopwords to remove
# --ism_txt (str) - text file with dict of multi word phrases associated with user
# --username (str) - name of target for output file

if len(sys.argv) > 1:
    input_csv = sys.argv[1]
    ism_txt = sys.argv[2]
    stopwords_txt = sys.argv[3]
    username = sys.argv[4]
else:
    input_csv = r'data\JustinTrudeau_clean.csv'
    ism_txt = r'meta\trudeauisms.txt'
    stopwords_txt = r'meta\stopwords.txt'
    username = 'JustinTrudeau'


def main():
    df = pd.read_csv(input_csv, encoding='utf-8')
    print(dt.datetime.today().strftime('%b-%d-%Y %H:%M:%S EST - ') +
          'Read ' + str(len(df)) + ' rows from file ' + input_csv)

    df['Tweets'].replace('', float('NaN'), inplace=True)
    df.dropna(subset=['Tweets'], inplace=True)

    get_word_freq(df)


def get_word_freq(df):
    # punctuation to strip from tweets (note omission of underscore)
    punctuation = '!"$%&\'\’“()*+,-./:;<=>?[\\]^`{|}~'
    english_stopwords = set(stopwords.words('english'))  # common uninteresting words
    # empirically added words to remove
    with open(stopwords_txt) as f:
        more_stopwords = set(literal_eval(f.read().strip('\n')))  # read extra stopwords from file, remove newline
    words_to_remove = more_stopwords.union(english_stopwords)  # all words to remove
    # want to count the following common phrases from our target as one word:
    common_phrases = {}
    with open(ism_txt) as f:
        for line in f:
            (key, val) = line.split(':')
            common_phrases[key] = val

    df['TweetsTokenized'] = [tokenize_tweet(t, common_phrases, punctuation, words_to_remove) for t in df['Tweets']]

    # -- create df of top 100 occurring words by month --
    keyword_freq = pd.DataFrame()
    for partition_method in ['Month', 'Quarter']:  # partition method must match a column header
        if partition_method == 'Month':
            period_list = ['January', 'February', 'March', 'April', 'May', 'June']
        elif partition_method == 'Quarter':
            period_list = ['Q1', 'Q2']
        for period in period_list:  # get top words from each month, create df
            period_abbr = period.lower()[0:3]  # first three letters of lowercase month (quarter unaffected)
            prd_tweets = df.loc[df[partition_method] == period]['TweetsTokenized']  # tweets from specific month
            print(dt.datetime.today().strftime('%b-%d-%Y %H:%M:%S EST - ') +
                  str(len(prd_tweets)) + ' tweets from @' + username + ' in ' + period)
            words = pd.Series(np.concatenate([tt for tt in prd_tweets])).value_counts()[0:100]
            keyword_freq['kw_'+period_abbr] = words.index
            keyword_freq['freq_'+period_abbr] = words.values
        words = pd.Series(np.concatenate([tt for tt in df['TweetsTokenized']])).value_counts()[0:100]
        last_partition = period_list[-1].lower()[0:3] + 'YTD'  # eg 'junYTD' or 'q2YTD'
        keyword_freq['kw_' + last_partition] = words.index
        keyword_freq['freq_' + last_partition] = words.values
        # -- save df and kw freq to csv --
        output_path_kw = os.path.join('data', 'kw_ana', username + '_' + partition_method + 's_words.csv')
        keyword_freq.to_csv(output_path_kw, header=True, encoding='utf-8', index=False)
        print(dt.datetime.today().strftime('%b-%d-%Y %H:%M:%S EST - ') +
              'Successfully wrote ' + str(len(keyword_freq)) + ' rows to \'' + output_path_kw + '\'')
    output_path_df = os.path.join('data', 'kw_ana', username + '_tokenized.csv')
    df.to_csv(output_path_df, header=True, encoding='utf-8', index=False)
    print(dt.datetime.today().strftime('%b-%d-%Y %H:%M:%S EST - ') +
          'Successfully wrote ' + str(len(df)) + ' rows to \'' + output_path_df + '\'')


def tokenize_tweet(tweet, common_phrases, punctuation, words_to_remove):
    tweet = str(tweet).lower()  # only want lowercase letters
    tweet = tweet.translate(str.maketrans('', '', punctuation))
    for orig, new in common_phrases.items():
        tweet = tweet.replace(orig, new)

    words = tweet.split(sep=' ')
    keywords = []
    for w in words:
        w = regex.sub(r'[^\p{Latin}{0-9}_#@]', '', w).strip()  # only keep latin chars, numbers, and '_', '#', '@'
        if len(w) > 0 and w not in words_to_remove and \
                (w.isalpha() or any(c.isdigit() for c in w) or any(p in w for p in '_#@')):
            # add if (1) not an undesirable word and (2) either no punctuation or contains only acceptable punctuation
            keywords.append(w)
    return keywords


if __name__ == '__main__':
    print(dt.datetime.today().strftime('%b-%d-%Y %H:%M:%S EST - ') +
          'STARTING program ' + sys.argv[0] + '...')
    main()

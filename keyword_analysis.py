import pandas as pd
import numpy as np
import sys
import os
from nltk.corpus import stopwords

if len(sys.argv) > 1:
    input_csv = sys.argv[1]
    ism_txt = sys.argv[2]
    username = sys.argv[3]
else:
    input_csv = r'data\JustinTrudeau_clean.csv'
    ism_txt = r'data\kw_ana\trudeauisms.txt'
    username = 'JustinTrudeau'


def main():
    df = pd.read_csv(input_csv, encoding='utf-8')

    df['Tweets'].replace('', float('NaN'), inplace=True)
    df.dropna(subset=['Tweets'], inplace=True)

    get_word_freq(df)


def get_word_freq(df):
    # punctuation to strip from tweets (note omission of underscore)
    punctuation = '!"$%&\'\’“()*+,-./:;<=>?[\\]^`{|}~'
    english_stopwords = set(stopwords.words('english'))  # common uninteresting words
    # empirically added words to remove
    more_stopwords = {'dont', 'get', 'make', 'even', 'also', 'time', 'said', 'far', 'amp', 'new', 'would', 'like', 'us',
                      'back', 'two', 'its', 'many', 'want', 'done', 'made', 'really', 'yet', 'got', 'nothing',
                      'ever', 'read', 'one', 'last', 'well', 'way', 'total', 'see', 'look', 'complete', 'didnt',
                      'keep', 'today', 'go', 'going', 'must', 'years', 'much', 'pm', 'always', 'first', 'day', 'let',
                      'know', 'open', 'others', 'better', 'small', 'say', 'need', 'come', 'long', 'doesnt', 'weve',
                      'wrong', 'happen', 'true', 'everything', 'getting', 'three', 'zero', 'fact', 'knew', 'sure',
                      'ago', 'including', 'already', 'right', 'every', 'things', 'never', 'fast', 'im', 'youre',
                      'thats', 'around', 'since', 'met', 'weve'}
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
    for m in ['January', 'February', 'March', 'April', 'May']:  # get top words from each month, create df
        mth = m.lower()[0:3]  # first three letters of lowercase month
        mth_tweets = df.loc[df['Month'] == m]['TweetsTokenized']  # tweets from specific month
        words = pd.Series(np.concatenate([tt for tt in mth_tweets])).value_counts()[0:100]
        keyword_freq['kw_'+mth] = words.index
        keyword_freq['freq_'+mth] = words.values
    words = pd.Series(np.concatenate([tt for tt in df['TweetsTokenized']])).value_counts()[0:100]
    keyword_freq['kw_all'] = words.index
    keyword_freq['freq_all'] = words.values
    # -- save df and kw freq to csv --
    output_path_df = os.path.join('data', 'kw_ana', username + '_tokenized.csv')
    df.to_csv(output_path_df, header=True, encoding='utf-8', index=False)
    output_path_kw = os.path.join('data', 'kw_ana', username + '_words.csv')
    keyword_freq.to_csv(output_path_kw, header=True, encoding='utf-8', index=False)


def tokenize_tweet(tweet, common_phrases, punctuation, words_to_remove):
    tweet = str(tweet).lower()  # only want lowercase letters
    tweet = tweet.translate(str.maketrans('','',punctuation))
    for orig, new in common_phrases.items():
        tweet = tweet.replace(orig, new)

    words = tweet.split(sep=' ')
    keywords = []
    for w in words:
        if w not in words_to_remove and (w.isalpha() or '_' in w or any(c.isdigit() for c in w)):
            # add if (1) not an undesirable word and (2) either no punctuation or contains only acceptable punctuation
            keywords.append(w)
    return keywords


if __name__ == '__main__':
    main()
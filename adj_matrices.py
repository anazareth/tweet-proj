import pandas as pd
import sys
import os
from ast import literal_eval

if len(sys.argv) > 1:
    input_csv = sys.argv[1]
    input_words = sys.argv[2]
    username = sys.argv[3]
else:
    input_csv = r'data\kw_ana\JustinTrudeau_tokenized.csv'
    input_words = r'data\kw_ana\JustinTrudeau_words.csv'
    username = 'JustinTrudeau'


def main():
    df = pd.read_csv(input_csv, encoding='utf-8')
    words_df = pd.read_csv(input_words, encoding='utf-8')
    for m in ['January', 'February', 'March', 'April', 'May', 'all']:
        mth = m.lower()[0:3]
        top100_words = list(words_df['kw_' + mth])
        if mth == 'all':
            mth_tweets = df['TweetsTokenized']
        else:
            mth_tweets = df.loc[df['Month'] == m]['TweetsTokenized']
        mth_tts = [literal_eval(i) for i in mth_tweets]
        create_matrix(mth, mth_tts, top100_words)


def create_matrix(mth, mth_tts, top100_words):
    top100_set = set(top100_words)
    adj_mat = pd.DataFrame(0, index=top100_words, columns=top100_words)  # weighted adjacency matrix (init with 0's)
    for tt in mth_tts:  # for each tweet
        tweet_words = set(tt) & top100_set  # set intersection (don't care about words outside top 100)
        for wrd in tweet_words:  # for each top100 word in the tweet
            wrd_pos = top100_words.index(wrd)
            remaining_words = set(tweet_words) - {wrd}
            for rem in remaining_words:  # for each other word in the tweet
                rem_pos = top100_words.index(rem)
                if rem_pos < wrd_pos:  # want consistent ordering so that adj matrix is upper triangular
                    adj_mat.loc[rem, wrd] = adj_mat.loc[rem, wrd] + 1
                else:
                    adj_mat.loc[wrd, rem] = adj_mat.loc[wrd, rem] + 1
    # -- save df to csv --
    output_path = os.path.join('data', 'kw_ana', username + '_adjmat_'+mth+'.csv')
    adj_mat.to_csv(output_path, header=True, encoding='utf-8', sep=';')


if __name__ == '__main__':
    main()

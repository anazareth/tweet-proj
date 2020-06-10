import pandas as pd
import sys
import os


if len(sys.argv) > 1:
    input_csv = sys.argv[1]
    ism_txt = sys.argv[2]
    username = sys.argv[3]
else:
    input_csv = r'data\kw_ana\JustinTrudeau_tokenized.csv'
    ism_txt = r'data\trudeauisms.txt'
    username = 'JustinTrudeau'


def main():
    df = pd.read_csv(input_csv, encoding='utf-8')
    for mth in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'all']:
        top100_words = list(df['kw_'+mth])
        mth_tweets = df.loc[df['Month']==mth]['Tweets']
        create_matrix(mth, mth_tweets, top100_words)


def create_matrix(mth, mth_tweets, top100_words):
    top100_set = set(top100_words)
    adj_mat = pd.DataFrame(0, index=top100_words, columns=top100_words)  # weighted adjacency matrix (init with 0's)
    for twt in mth_tweets:  # for each tweet
        # set intersection (don't care about words outside top 100)
        tweet_words = set(tokenize_tweet(twt)) & top100_set
        for wrd in tweet_words:  # for each word in the tweet
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
    adj_mat.to_csv(output_path, header=True, encoding='utf-8', index=False, sep=';')


if __name__ =='__main__':
    main()

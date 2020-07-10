import pandas as pd
import sys
import os
from ast import literal_eval
import datetime as dt

# adj_matrices.py input_csv input_words username
# --input_csv (str) - name of csv file (and path if necessary)
# --input_words (str) - csv file with monthly top100 words
# --username (str) - name of target for output file

if len(sys.argv) > 1:
    input_csv = sys.argv[1]
    input_words = sys.argv[2]
    username = sys.argv[3]
else:
    input_csv = r'data\kw_ana\JustinTrudeau_tokenized.csv'
    input_words = r'data\kw_ana\JustinTrudeau_Months_words.csv'
    username = 'JustinTrudeau'


def main():
    df = pd.read_csv(input_csv, encoding='utf-8')
    words_df = pd.read_csv(input_words, encoding='utf-8')
    print(dt.datetime.today().strftime('%b-%d-%Y %H:%M:%S EST - ') +
          'Read ' + str(len(df)) + ' rows from file ' + input_csv)

    if 'months' in input_words.lower():
        partition_method = 'Month'
    else:
        partition_method = 'Quarter'

    if partition_method == 'Month':
        period_list = ['January', 'February', 'March', 'April', 'May', 'June']
    elif partition_method == 'Quarter':
        period_list = ['Q1', 'Q2']
    for period in period_list:
        period_abbr = period.lower()[0:3]
        top100_words = list(words_df['kw_' + period_abbr])
        prd_tweets = df.loc[df[partition_method] == period]['TweetsTokenized']
        prd_tts = [literal_eval(i) for i in prd_tweets]
        create_matrix(period_abbr, prd_tts, top100_words)
    period_abbr = period_list[-1].lower()[0:3] + 'YTD'  # now for all tweets
    top100_words = list(words_df['kw_' + period_abbr])
    prd_tweets = df['TweetsTokenized']
    prd_tts = [literal_eval(i) for i in prd_tweets]
    create_matrix(period_abbr, prd_tts, top100_words)


def create_matrix(period_abbr, prd_tts, top100_words):
    top100_set = set(top100_words)
    adj_mat = pd.DataFrame(0, index=top100_words, columns=top100_words)  # weighted adjacency matrix (init with 0's)
    for tt in prd_tts:  # for each tweet
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
    output_path = os.path.join('data', 'kw_ana', username + '_adjmat_' + period_abbr + '.csv')
    adj_mat.to_csv(output_path, header=True, encoding='utf-8', sep=';')
    print(dt.datetime.today().strftime('%b-%d-%Y %H:%M:%S EST - ') +
          'Successfully wrote ' + str(len(adj_mat)) + ' rows to \'' + output_path + '\'')


if __name__ == '__main__':
    print(dt.datetime.today().strftime('%b-%d-%Y %H:%M:%S EST - ') +
          'STARTING program ' + sys.argv[0] + '...')
    main()

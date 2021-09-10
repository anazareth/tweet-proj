import argparse
import os
import numpy as np
import datetime as dt
import mysql.connector
import pandas as pd
from sqlalchemy import create_engine


def main(args):
    srvr_endpt, srvr_user, srvr_pass = np.loadtxt('shhh.txt', delimiter='\n', dtype=str)[-3:]
    # tweetdb = mysql.connector.connect(
    #     host=srvr_endpt,
    #     user=srvr_user,
    #     password=srvr_pass
    # )
    # tdb_cursor = tweetdb.cursor()

    tweetdb = create_engine('mysql+mysql.connector://admin:'+srvr_pass+'@'+srvr_endpt+':3306/')

    if tweetdb is not None:
        print('Successfully connected to database.')
    if args.username == 'all':
        for fname in os.listdir('data'):
            if fname.endswith('_clean.csv') and 'sample' not in fname.split('_'):
                # TODO: read file and upload
                df = pd.read_csv('data\\data' + fname, headers=True)
                df.to_sql(con=tweetdb, name='Tweets', if_exists='append')
                print(dt.datetime.today().strftime('%b-%d-%Y %H:%M:%S EST - ') +
                    'Uploaded ' + len(df) + ' rows from file ' + fname)
    else:
        fname = args.username + '_clean.csv'
        df = pd.read_csv('data\\' + fname)
        df.to_sql(con=tweetdb, name='Tweets', if_exists='append')
        
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Upload tweet data (_clean.csv files) to sql server.')
    parser.add_argument('-u', '--username', help='twitter handle of user, default all', default='JustinTrudeau', required=False)
    print(dt.datetime.today().strftime('%b-%d-%Y %H:%M:%S EST - ') +
          'STARTING program ' + parser.prog + '...')
    args = parser.parse_args()
    main(args)
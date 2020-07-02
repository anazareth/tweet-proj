import argparse
import community as community_louvain
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import os
import datetime as dt


# louvain_partition.py username
# --username (str) - twitter handle of target, eg. JustinTrudeau
# NOTE: assume adjacency matrix csv stored under data/kw_ana/username_adjmat_mth.csv


def main(args):
    username = args.username
    if args.matfile is not None:
        file_list = list(args.matfile)
    else:  # loop through all months
        file_list = [os.path.join('data', 'kw_ana', username + '_adjmat_' + m + '.csv') for m in
                     ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'all']]
    for file_path in file_list:
        df = pd.read_csv(file_path, delimiter=';', index_col=0)

        top100_list = list(df.columns)

        ntwrk = nx.Graph()  # create graph object
        ntwrk.add_nodes_from(top100_list)  # add nodes from index of adjacency matrix

        # add weighted edges iteratively - i and j are indices (row and column essentially)
        for i in range(len(top100_list)):
            for j in range(i, len(top100_list)):  # recall matrix is upper triangular
                if df.iloc[i, j] != 0:
                    ntwrk.add_edge(top100_list[i], top100_list[j], weight=df.iloc[i, j])
        file_name = os.path.split(file_path)[-1]  # last element of path is file name only
        find_communities(ntwrk, file_name, username)


def find_communities(network, month, username):
    # find most likely number of commnunities, since there is an element of randomness to the Louvain algorithm
    N = 100  # number of times to run Louvain
    iter_tracking = {k: 0 for k in range(2, 25)}
    for i in range(N):
        partition = community_louvain.best_partition(network, resolution=1.05)  # compute best partition
        num_partitions = max(partition.values()) + 1  # communities labelled 0 to k-1, where k is number of communities
        iter_tracking[num_partitions] += 1  # increment counter
    # f is frequency of partition; N/3 is set threshold; don't want less than 4 communities
    close_values = [f for f in iter_tracking.values() if f > N / 3]
    # if it's close, take the lower number of communities, minimum 3 (3 ok in non-"tiebreaker" situations)
    close_keys = [k for k in iter_tracking.keys() for f in close_values if f == iter_tracking[k]]
    close_keys_gt3 = [k for k in close_keys if k > 3]
    num_communities = min(close_keys_gt3) if len(close_keys_gt3) != 0 else min(close_keys)
    pct_certain = iter_tracking.get(num_communities)/N
    print(dt.datetime.today().strftime('%b-%d-%Y %H:%M:%S EST - ') +
          'Found ' + str(num_communities) + ' communities in file \'' + month + '\' (' + str(pct_certain) + ').')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process user/file info for community detection.')
    parser.add_argument('-u', '--username', help='twitter handle of user', default='JustinTrudeau', required=True)
    parser.add_argument('-M', '--matfile', help='adjacency matrix for desired month')
    print(dt.datetime.today().strftime('%b-%d-%Y %H:%M:%S EST - ') +
          'STARTING program ' + parser.prog + '...')
    args = parser.parse_args()
    main(args)

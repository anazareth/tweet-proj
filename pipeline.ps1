$username = $args[0]
python scraper.py $username 1212268323691532289 1267229979449966594
python clean_tweets.py data\$username'_raw.csv' 1 $username
python keyword_analysis.py data\$username'_clean.csv' meta\blankisms.txt meta\nostopwords.txt $username
python adj_matrices.py data\kw_ana\$username'_tokenized.csv' data\kw_ana\$username'_words.csv' $username
python louvain_partition.py -u $username
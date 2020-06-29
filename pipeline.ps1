$username = $args[0]
python scraper.py $username 1212268323691532289 1267229979449966594
Write-Output '--------------------------------------------------------------------------------------'
python clean_tweets.py data\$username'_raw.csv' 1 $username
Write-Output '--------------------------------------------------------------------------------------'
python keyword_analysis.py data\$username'_clean.csv' meta\blankisms.txt meta\stopwords.txt $username
Write-Output '--------------------------------------------------------------------------------------'
python adj_matrices.py data\kw_ana\$username'_tokenized.csv' data\kw_ana\$username'_words.csv' $username
Write-Output '--------------------------------------------------------------------------------------'
python louvain_partition.py -u $username
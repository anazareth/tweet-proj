$username = $args[0]
if ( $username -ne 'realDonaldTrump' ) {
	# scraper doesn't work for donald trump, but everything else works
	python scraper.py $username 1212268323691532289 1267229979449966594
}
if ( $username -eq 'realDonaldTrump' ) {
	$ismtxt = 'trumpisms.txt'
} elseif ( $username -eq 'JustinTrudeau' ) {
	$ismtxt = 'trudeauisms.txt'
} else {
	$ismtxt = 'blankisms.txt'
}
Write-Output '--------------------------------------------------------------------------------------'
python clean_tweets.py data\$username'_raw.csv' 1 $username
Write-Output '--------------------------------------------------------------------------------------'
python keyword_analysis.py data\$username'_clean.csv' meta\$ismtxt meta\stopwords.txt $username
Write-Output '--------------------------------------------------------------------------------------'
python adj_matrices.py data\kw_ana\$username'_tokenized.csv' data\kw_ana\$username'_words.csv' $username
Write-Output '--------------------------------------------------------------------------------------'
python louvain_partition.py -u $username
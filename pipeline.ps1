$username = $args[0]
Write-Output '--------------------------------------------------------------------------------------'
Write-Output "Beginning processing for $username"
Write-Output '--------------------------------------------------------------------------------------'
if ( $username -ne 'realDonaldTrump' -and $username -notlike '*sample*' -and $username -notlike '*random*' ) {
	# scraper doesn't work for donald trump, but everything else works
	python scraper.py $username 1212268323691532289 1278078666942173184
}
else {
	Write-Output('Bypassing scraper stage...')
}
if ( $username -eq 'realDonaldTrump' ) {
	$ismtxt = 'trumpisms.txt'
} elseif ( $username -eq 'JustinTrudeau' ) {
	$ismtxt = 'trudeauisms.txt'
} else {
	$ismtxt = 'blankisms.txt'
}
Write-Output '--------------------------------------------------------------------------------------'
if ($username -notlike '*sample*') {
python clean_tweets.py data\$username'_raw.csv' 1 $username
}
else {
	Write-Output('Bypassing clean_tweets stage...')
}
Write-Output '--------------------------------------------------------------------------------------'
python keyword_analysis.py data\$username'_clean.csv' meta\$ismtxt meta\stopwords.txt $username
Write-Output '--------------------------------------------------------------------------------------'
python adj_matrices.py data\kw_ana\$username'_tokenized.csv' data\kw_ana\$username'_Quarters_words.csv' $username
python adj_matrices.py data\kw_ana\$username'_tokenized.csv' data\kw_ana\$username'_Months_words.csv' $username
Write-Output '--------------------------------------------------------------------------------------'
python louvain_partition.py -u $username
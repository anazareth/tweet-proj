# tweet-proj

## About

This is the code used to gather Tweets from 700+ political American and Canadian political figures over 2020 for my MSc thesis, successfully defended August, 2021. Processing of the data involved removing retweets, non-english tweets, and non-text tweets. Data analysis was done through creation of 100x100 keyword networks for each politician in a given month, and running the Louvain community detection algorithm. We also wrote and presented a paper on the subject which was accepted to Complex Networks 2021, read here: https://arxiv.org/abs/2108.13259.

My powershell script runs the following Python scripts in order (each feeding off the output of the last). Initial input is Twitter username and date range, final output is adjacency matrices of top 100 keywords for each month. Other files are generated along the way, such as "clean" tweets.
 
**scraper.py** - connect to Twitter API (using my secret credentials) and pull a range of tweets (by tweet id) from
		a specified user; output CSV with metadata eg. 'tweet_out//trudeau_raw.csv'
		USAGE:
		python scraper.py username start_id end_id
			--username (string) - target twitter handle
			--start_id (int) - tweet id (found in URL) of earliest tweet desired
			--end_id (int) - tweet id (found in URL) of final tweet desired
		
**clean_tweets.py** - input raw data from output csv from scraper.py (or trump archive);
		drop french tweets and RTs (optional);
		save to CSV with columns: Tweets, Length, Date, Source, Favourites, RTs, Language, isRT, Month
		eg. 'data//JustinTrudeau_clean.csv'
		USAGE:
		python clean_tweets.py input_csv remove_rts username
			--input_csv (str) - name of csv file (and path if necessary). Note that output file will go in same location.
			--remove_rts (int) - boolean (0=false, 1=True) if RTs should be removed or not
			--username (str) - name of target for output file: realDonaldTrump or JustinTrudeau, others in future


**keyword_analysis.py** - input csv generated from clean_tweets.py; remove stopwords, find common phrases;
		get frequency of words by month and user; 
		output kws to csv eg. 'data//JustinTrudeau_words.csv';
		output df with tokenized tweets column to csv eg. 'data//JustinTrudeau_tokenized.csv';
		USAGE:
		keyword_analysis.py data//trudeau_clean.csv ism_txt username
			--with arguments:
			--input_csv (str) - name of csv file (and path if necessary)
			--ism_txt (str) - text file with dict of multi word phrases associated with user
			--username (str) - name of target for output file
		
**adj_matrices.py** - input df with tokenized column eg. 'data//JustinTrudeau_tokenized.csv';
		create adjacency matrix for each month and all months, output csv files
		eg. 'data//kw_ana//JustinTrudeau_adjmat_may.csv'
		USAGE:
		adj_matrices.py input_csv input_words username
		--input_csv (str) - name of csv file (and path if necessary)
		--input_words (str) - csv file with monthly top100 words
		--username (str) - name of target for output file
		
## Other
**word_data_analysis.py** - calculate frequency of covid mentions in tweets of governors

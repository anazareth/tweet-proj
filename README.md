# tweet-proj
 twitter scraping and analysis
 
scraper.py - connect to Twitter API (using my secret credentials) and pull a range of tweets (by tweet id) from
		a specified user; output CSV with metadata eg. 'tweet_out//trudeau_raw.csv'

clean_tweets.py - input raw data from output csv from scraper.py (or trump archive);
		drop french tweets and RTs (optional);
		save to CSV with columns: Tweets, Length, Date, Source, Favourites, RTs, Language, isRT, Month
		eg. 'data//JustinTrudeau_clean.csv'

keyword_analysis.py - input csv generated from clean_tweets.py; remove stopwords, find common phrases;
		get frequency of words by month and user; 
		output kws to csv eg. 'data//JustinTrudeau_words.csv';
		output df with tokenized tweets column to csv eg. 'data//JustinTrudeau_tokenized.csv';
		
adj_matrices.py - input df with tokenized column eg. 'data//JustinTrudeau_tokenized.csv';
		create adjacency matrix for each month and all months, output csv files
		eg. 'data//kw_ana//JustinTrudeau_adjmat_may.csv'

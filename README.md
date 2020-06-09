# tweet-proj
 twitter scraping and analysis
 
scraper.py - connect to Twitter API (using my secret credentials) and pull a range of tweets (by tweet id) from
		a specified user; output CSV with metadata eg. 'tweet_out//trudeau_raw.csv'

prepare_tweets.ipynb - input raw data from output csv from scraper.py; drop non-english tweets and RTs;
		save to CSV with columns: Tweets, Length, Date, Source, Favourites, RTs, Language, isRT, Month
		eg. 'data//trudeau_clean.csv'

prepare_trump.ipynb - input raw data from Trump Twitter Archive; drop RTs;
		save new tweets to CSV 'data//trump_clean.csv' with columns: 
		Tweets, Length, Date, Source, Favourites, RTs, Language, isRT, id_str, Month

keyword_analysis.ipynb - input csv generated from prepare_tweets.ipynb; remove stopwords, find common phrases;
		get frequency of words by month and user; output to csv eg. 'data//trudeau_words.csv'

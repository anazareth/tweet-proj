# tweet-proj
 twitter scraping and analysis
 
scraper.py - connect to Twitter API (using my secret credentials) and pull a range of tweets (by tweet id) from
		a specified user; output CSV with metadata eg. 'tweet_out//trudeau_raw.csv'

prepare_tweets.ipynb - input raw data from output csv from scraper.py; drop non-english tweets and RTs;
		save to CSV with columns: Tweets, Length, Date, Source, Favourites, RTs, Language, isRT, Month
		eg. 'data//trudeau_jfma.csv'

keyword_analysis.ipynb - input csv generated from prepare_tweets.ipynb; remove stopwords, find common phrases;
		get frequency of words by month and user; output to csv eg. 'data//trudeau_words.csv'

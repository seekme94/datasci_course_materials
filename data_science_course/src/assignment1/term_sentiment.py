# This script scans tweets from a file and calculates sentiment score of words unavailable in intput file

import sys
import json

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])

    scores = {} # initialize an empty dictionary
    tweets = {}
    tweet_scores = {}
    new_scores = {}
    for line in sent_file:
        term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        scores[term] = int(score)  # Convert the score to an integer.

    for line in tweet_file:
        tweet = json.loads(line) # Returns a dict object into tweet
        tweet_text = tweet.get("text")
        if tweet_text == None:
            continue
        tweet_text = tweet_text.lower() # Returns tweet text in lower text
        tweet_id = tweet.get("id")
        tweets[tweet_id] = tweet_text

    for tweet in tweets:
        words = tweets[tweet].split(" ")
        sent_score = 0
        for word in words:
            word = ''.join(e for e in word if e.isalnum()) # Removes all special characters from a word
            score = scores.get(word.lower()) # Turn to lower case for better matches
            if score != None:
                sent_score = sent_score + int(score) # Add score to total sentiment score
            else:
                new_scores[word] = 0 # Neutralize the words that aren't in sentiment file
        tweet_scores[tweet] = sent_score # Save sentiment score of each tweet

    # For every word, scan all tweets the word occurs in and sum the sentiments of all these tweets
    for word in new_scores:
        sent_score = 0
        for tweet in tweets:
            tweet_text = tweets[tweet]
            if tweet_text.find(word) != -1:
                sent_score = sent_score + tweet_scores[tweet]
        word = word.encode('cp850', errors='replace')
        print(str(word) + " " + str(sent_score))

if __name__ == '__main__':
    main()


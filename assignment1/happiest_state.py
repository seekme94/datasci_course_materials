# This script analyzes sentiments in tweet stream file and computes which state of the US-states is the happiest in terms of sentiments

import sys
import json

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])

    happiness = {}  # initialize an empty dictionary
    tweets = {}
    scores = {}
    for line in sent_file:
        term, score = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        scores[term] = int(score)  # Convert the score to an integer.

    for line in tweet_file:
        tweet = json.loads(line)  # Returns a dict object into tweet
        if tweet.__contains__("text"):
            tweet_text = tweet.get("text").lower()  # Returns tweet text in lower text
            tweet_id = tweet.get("id")
            if tweet.__contains__("place"):
                tweet_place = tweet.get("place")
                place_dump = json.dumps(tweet_place)
                place = json.loads(place_dump)
                if place != None:
                    print place
            tweets[tweet_id] = tweet_text

if __name__ == '__main__':
    main()

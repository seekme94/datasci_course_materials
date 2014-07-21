# This script calculates terms in tweet stream file (# of occurrences of the term in all tweets]/[# of occurrences of all terms in all tweets)

import sys
import json

def main():
    tweet_file = open(sys.argv[1])

    frequencies = {}  # initialize an empty dictionary
    tweets = {}
    for line in tweet_file:
        tweet = json.loads(line)  # Returns a dict object into tweet
        tweet_text = tweet.get("text").lower()  # Returns tweet text in lower text
        tweet_id = tweet.get("id")
        tweets[tweet_id] = tweet_text

    for tweet in tweets:
        words = tweets[tweet].split(" ")
        for word in words:
            word = ''.join(e for e in word if e.isalnum())
            frequencies[word] = 0.0

    for word in frequencies:
        frequency = 0.0
        for tweet in tweets:
            tweet_text = tweets[tweet]
            frequency = frequency + tweet_text.count(word)
        frequencies[word] = frequency / len(frequencies.items())
        print word + " " + str(frequencies[word])

if __name__ == '__main__':
    main()

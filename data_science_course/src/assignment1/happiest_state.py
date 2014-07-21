# This script analyzes sentiments in tweet stream file and computes which state of the US-states is the happiest in terms of sentiments

import sys
import json

def out (x):
    print(str(x).encode('cp850', errors='replace'))

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])

    states = {'USA','AL','AK','AZ','AR','CA','CO','CT','DE','FL','GA','HI','ID','IL','IN','IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VT','VA','WA','WV','WI','WY'}
    happiness = {}  # initialize an empty dictionary
    tweets = {}
    scores = {}
    for state in states:
        happiness[state] = 0.0
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
                    country_code = place.get("country_code")
                    if country_code == 'US': # Since only residents of USA have sentiments
                        full_name = place.get("full_name")
                        city, state = full_name.split(", ")
                        happiness[state] = happiness[state] + 0 # Compute tweet sentiment
            tweets[tweet_id] = tweet_text

if __name__ == '__main__':
    main()

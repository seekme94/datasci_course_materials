# This script analyzes sentiments in tweet stream file and computes which state of the US-states is the happiest in terms of sentiments

import sys
import json

def out (x):
    print(str(x).encode('cp850', errors='replace'))

def calculate_tweet_score (tweet_text, scores):
    words = tweet_text.split(" ")
    sent_score = 0.0
    for word in words:
      word = ''.join(e for e in word if e.isalnum())  # Removes all special characters from a word
      score = scores.get(word.lower())  # Turn to lower case for better matches
      if score != None:
        sent_score = sent_score + int(score)  # Add score to total sentiment score
    return sent_score

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])

    states = {'USA', 'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'}
    happiness = {}  # Initialize empty dictionary
    tweets = {}
    scores = {}

    # Save term scores
    for line in sent_file:
        term, score = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        scores[term] = int(score)  # Convert the score to an integer.

    # Initiate happiness score of each state
    for state in states:
        happiness[state] = 0.0

    # Scan every tweet; process those having place
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
                    if country_code == 'US':  # Since only residents of USA have sentiments
                        full_name = place.get("full_name")
                        city, state = full_name.split(", ")
                        tweet_sent = float(calculate_tweet_score(tweet_text, scores))  # Compute tweet sentiment
                        happiness[state] = happiness[state] + tweet_sent
    max_score = 0.0
    happy_state = ''
    for state in happiness:
        if happiness[state] > max_score:
            happy_state = state
            max_score = happiness[state]
#        print(state + " " + str(happiness[state]))
    print(happy_state)
if __name__ == '__main__':
    main()

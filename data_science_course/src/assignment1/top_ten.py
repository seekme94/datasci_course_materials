# This script analyzes sentiments in tweet stream file and computes which state of the US-states is the happiest in terms of sentiments

import sys
import json

def out (x):
    print(str(x).encode('cp850', errors='replace'))

def main():
    tweet_file = open(sys.argv[1])

    hashtags = {}

    # Scan every tweet; process those having hashtags
    for line in tweet_file:
        tweet = json.loads(line)  # Returns a dict object into tweet
        if tweet.__contains__("text"):
            if tweet.__contains__("entities"):
                # Extract entitites
                tweet_hashtags = tweet.get("entities")
                # Extract hashtags arrays from entities
                hashtag_list = tweet_hashtags.get("hashtags")
                for tag in hashtag_list:
                    # Only non-empty lists
                    if len(tag) > 0:
                        text = tag.get("text")
                        #text = text.encode('ascii', 'ignore')
                        count = 0
                        try:
                            count = hashtags[text]
                        except KeyError:
                            None
                        hashtags[text] = count + 1
    # Sort it out, get top 10
    vals = sorted(hashtags.values(), reverse=True)
    # Top 10 values only
    vals = vals[:10]
    hashset = list()
    for i in vals:
        for item in (hashtags.items()):
            key, value = item
            if value == i:
                hashset.append(str(value) + " " + str(key))
    for item in hashset:
        value, key = item.split(" ")
        print (key + " " + value)
if __name__ == '__main__':
    main()

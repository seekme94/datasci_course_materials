# This script scans tweets from a file and calculates sentiment score by summing sentiment score of all words

import sys
import json

def main():
  sent_file = open(sys.argv[1]) # Sentiment scores
  tweet_file = open(sys.argv[2])

  scores = {} # initialize an empty dictionary
  for line in sent_file:
    term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
    scores[term] = int(score)  # Convert the score to an integer.
#    print scores.items() # Print every (term, score) pair in the dictionary

  for line in tweet_file:
    tweet = json.loads(line) # Returns a dict object into tweet
    tweet_text = tweet.get("text") # Returns tweet text
    if tweet_text == None:
        continue
    words = tweet_text.split(" ")
    sent_score = 0
    for word in words:
      word = ''.join(e for e in word if e.isalnum()) # Removes all special characters from a word
      score = scores.get(word.lower()) # Turn to lower case for better matches
      if score != None:
        sent_score = sent_score + int(score) # Add score to total sentiment score
    print(str(sent_score))

if __name__ == '__main__':
    main()


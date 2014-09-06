# This script analyzes sentiments in tweet stream file and computes which state of the US-states is the happiest in terms of sentiments

from datetime import datetime
import time
import json
import csv

def encode (x):
    return (str(x).encode('cp850', errors='replace'))

def get_tweet_data(tweet):
    data = {}
    # Tweet Id
    if tweet.__contains__("id"):
        data["tweet_id"] = tweet.get("id")
    # Timestamp
    if tweet.__contains__("created_at"):
        created_at = tweet.get("created_at")
        created_dt = datetime.strptime(created_at,'%a %b %d %H:%M:%S +0000 %Y')
        data["timestamp"] = time.mktime(created_dt.timetuple())
    # Language
    if tweet.__contains__("lang"):
        data["lang"] = tweet.get("lang")
    # User Id, Screen name and location
    if tweet.__contains__("user"):
        tweet_user = tweet.get("user")
        user_dump = json.dumps(tweet_user)
        user = json.loads(user_dump)
        if user != None:
            data["user_id"] = user.get("id")
            data["screen_name"] = user.get("screen_name")
            data["location"] = user.get("location")
            data["time_zone"] = user.get("time_zone")
    # Text
    if tweet.__contains__("text"):
        data["text"] = tweet.get("text")
    # In reply to user
    if tweet.__contains__("in_reply_to_screen_name"):
        data["in_reply_to_screen_name"] = tweet.get("in_reply_to_screen_name")
    # Retweeted?
    if tweet.__contains__("retweeted"):
        data["retweeted"] = tweet.get("retweeted")
    data["hashtags"] = get_hashtages(tweet)
    return data

def get_followers_data(follower):
    id_list = ""
    if follower.__contains__("ids"):
        id_list = follower.get("ids")
        if len(id_list) == 0:
            return None
    return id_list

# Hashtags > 1; 2; 3; ...
def get_hashtages(tweet):
    hashtags = ""
    if tweet.__contains__("entities"):
        tweet_entities = tweet.get("entities")
        entities_dump = json.dumps(tweet_entities)
        entities = json.loads(entities_dump)
        if entities != None:
            if entities.__contains__("hashtags"):
                tags = entities.get("hashtags")
                if len(tags) == 0:
                    return None
                for tag in tags:
                    tag_dump = json.dumps(tag)
                    hashtag = json.loads(tag_dump)
                    hashtags = hashtags + hashtag.get("text") + ";"
    return hashtags

def parse_stream_data(in_file, out_file):
    tweet_file = open(in_file)
    header = ['tweet_id', 'user_id', 'screen_name', 'text', 'hashtags', 'retweeted', 'location', 'in_reply_to_screen_name', 'time_zone', 'lang', 'timestamp']

    with open(out_file, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow(header)
        for line in tweet_file:
            tweet_obj = json.loads(line)
            tweet = get_tweet_data(tweet_obj)
            tweet_row = []
            for column in header:
                value = tweet.get(column)
                tweet_row.append(value)
            writer.writerow(tweet_row)

def parse_followers_data(in_file, out_file):
    tweet_file = open(in_file)
    header = ['tweet_id', 'user_id', 'screen_name', 'text', 'hashtags', 'retweeted', 'location', 'in_reply_to_screen_name', 'time_zone', 'lang', 'timestamp']

    with open(out_file, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow(header)
        for line in tweet_file:
            tweet_obj = json.loads(line)
            tweet = get_tweet_data(tweet_obj)
            tweet_row = []
            for column in header:
                value = tweet.get(column)
                tweet_row.append(value)
            writer.writerow(tweet_row)

if __name__ == '__main__':
    in_file = "/home/owais/Datasets/afridi_tweets.txt"
    out_file = "/home/owais/Datasets/afridi_tweets.csv"
    parse_stream_data(in_file, out_file)
    parse_followers_data(in_file, out_file)

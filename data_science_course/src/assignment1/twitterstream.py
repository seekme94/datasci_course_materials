import oauth2 as oauth
import urllib2 as urllib
import sys
import csv
import time

# See assignment1.html instructions or README for how to get these credentials

api_key = "5AfUpboAL1NZSlpAh1XvQ"
api_secret = "uKAMIvyikyIVJaVj34oKuoXxk7BnrEklcTSjAWZk"
access_token_key = "130064601-uAozYOgna3WP5ImIpnHPl9QoneyqJxnCcif91jfk"
access_token_secret = "3NG0a0j2Wc4nGh4Ux8m0MvAngVzhTScxE96qnZgqceAHb"

_debug = 0

oauth_token = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=api_key, secret=api_secret)

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_method = "GET"


http_handler = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)

'''
Construct, sign, and open a twitter request
using the hard-coded credentials above.
'''
def twitterreq(url, method, parameters):
  req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                             token=oauth_token,
                                             http_method=http_method,
                                             http_url=url,
                                             parameters=parameters)

  req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

  headers = req.to_header()

  if http_method == "POST":
    encoded_post_data = req.to_postdata()
  else:
    encoded_post_data = None
    url = req.to_url()

  opener = urllib.OpenerDirector()
  opener.add_handler(http_handler)
  opener.add_handler(https_handler)

  response = opener.open(url, encoded_post_data)

  return response

def fetch_stream(q):
  url = "https://stream.twitter.com/1/statuses/sample.json?q=" + q
  
  parameters = []
  response = twitterreq(url, "GET", parameters)
  for line in response:
    print(line.strip())

def fetch_follower_id_stream(user_id):
  url = "https://api.twitter.com/1.1/followers/ids.json?cursor=-1&user_id=" + user_id
  
  parameters = []
  response = twitterreq(url, "GET", parameters)
  for line in response:
    response = line.strip()
    if "Rate limit exceeded" in response:
      time.sleep(60)
    print(response)

def fetch_user(user_id):
  url = "https://api.twitter.com/1.1/users/show.json?entities=false&user_id=" + user_id
  
  parameters = []
  response = twitterreq(url, "GET", parameters)
  for line in response:
    print(line.strip())

if __name__ == '__main__':
    # -s = stream data, -f = followers, -u = user
    command = "-x"
    query = ""

    with open("/home/owais/Datasets/afridi_nodes.txt", 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        header = reader.next()
        for row in reader:
            command = "-f"
            query = row[0]
            fetch_follower_id_stream(query)

    if len(sys.argv) > 1:
        command = sys.argv[1]
        query = sys.argv[2]
    if command == "-s":
        fetch_stream(query)
    elif command == "-f":
        fetch_follower_id_stream(query)
    elif command == "-u":
        fetch_user(query)

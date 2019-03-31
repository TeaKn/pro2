#!/usr/bin/python
# coding=utf8

from Pii import *
from time import *
import tweepy as tpy
import logging as log

# defines consumer and access keys for Twitter API

CONSUMER_KEY = "<your Twitter consumer key>"
CONSUMER_SECRET = "<your Twitter consumer secret>"

ACCESS_TOKEN = "<your Twitter access token>"
ACCESS_SECRET = "<your Twitter access secret>"

# sets up authentication and control of Twitter API

auth = tpy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tpy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True, compression = True)

# sets up basic logging facility for Twitter API

log.basicConfig(level = log.INFO)

start = time()

# defines seed user and number of nodes for Twitter followers graph

SEED = 'lovrosubelj'

N = 10000

# crawls Twitter followers graph for selected seed user

D = {SEED: 0}
Q = [SEED]
A = [[]]

while Q:
  s = Q.pop(0)
  
  try:
    for id in api.followers_ids(s):
      l = api.get_user(id).screen_name.encode('utf8')
      
      if l not in D:
        D[l] = len(D)
        A.append([])
        Q.append(l)
      
      A[D[s]].append(D[l])
      A[D[l]].append(D[s])

      print("'{0:s}' ({1:d}) | '{2:s}' ({3:d})".format(s, D[s], l, D[l]))
  except tpy.TweepError:
    print("Tweepy error occurred")

  if len(D) > N:
    break

# constructs Twitter followers graph for selected seed user

L = [None] * len(D)
for i, l in enumerate(D):
  L[i] = l

G = (SEED, A, L)

# prints out standard information of Twitter followers graph

info(G)

# stores Twitter followers graph to file in Pajek format

write(G)

print("{0:>12s} | {1:.1f} sec\n".format('Time', time() - start))

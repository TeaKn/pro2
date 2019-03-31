#!/usr/bin/python
# coding=utf8

from time import *
import requests
import re

# defines keys for Google Search, Maps and Translate API-s

GOOGLE_KEY = "<your Google key>"
GOOGLE_ID = "<your Google id>"

def pages(city):
  """
  Get the number of web pages about given Slovenian city using Google Search API.
  """
  req = requests.get('https://www.googleapis.com/customsearch/v1?q=' + re.sub(r'\s', '+', city) + ',+Slovenia&cx=' + GOOGLE_ID + '&key=' + GOOGLE_KEY).json()
  return int(req['searchInformation']['totalResults']) if 'searchInformation' in req else 0

def location(city):
  """
  Get the latitue and longitude of given Slovenian city using Google Maps API.
  """
  loc = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=' + re.sub(r'\s', '+', city) + ',+Slovenia&key=' + GOOGLE_KEY).json()['results'][0]['geometry']['location']
  return (loc['lat'], loc['lng'])

def synonym(word):
  """
  Find a synonym for given Slovenian word match by scrapping Kontekst.io web page.
  If the given word is capitalized, the returned synonym is also capitalized.
  """
  word = word.group()
  res = re.search(r'<a class="dictentry" href="/kontekst/[a-zčšž]+"> [a-zčšž]+ </a>', requests.get('https://kontekst.io/kontekst/' + word.lower()).text)
  syn = word if res is None else re.sub(r'<.*?>|\s', '', res.group())
  return syn.capitalize() if word == word.capitalize() else syn

def translate(text, target = 'en'):
  """
  Translate given Slovenian text into the specified language using Google Translate API.
  """
  return requests.get('https://translation.googleapis.com/language/translate/v2?q=' + re.sub(r'\s', '+', text) + '&source=sl&target=' + target + '&key=' + GOOGLE_KEY).json()['data']['translations'][0]['translatedText'].encode('utf8')

start = time()

# gets list of all Slovenian cities and their ZIP codes using Dejan Lavbič's API

cities = [city for city in requests.get('https://api.lavbic.net/kraji').json() if 'kraj' in city]

# prints out names, ZIP codes, GPS locations and number of web pages for Slovenian cities

for city in cities:
  loc = location(city['kraj'])
  print("{0:>12s} | {1:d}".format('ZIP', city['postnaStevilka']))
  print("{0:>12s} | '{1:s}, Slovenija'".format('City', city['kraj'].encode('utf8')))
  print("{0:>12s} | ({1:.3f}, {2:.3f})".format('Location', loc[0], loc[1]))
  print("{0:>12s} | {1:,d}\n".format('Google', pages(city['kraj'])))

print("{0:>12s} | {1:.1f} sec\n".format('Time', time() - start))

start = time()

# list of ten arbitrarily selected Slovenian proverbs

proverbs = ['Vse je šlo za med.', 'Jezik z mošnjo raste.', 'Lakota je najboljši kuhar.', 'Za prepir sta potrebna dva.', 'En cvet še ne naredi pomladi.', 'Rožnik deževen viničar reven.', 'Visokim smrekam vihar vrhove lomi.', 'Odloženo delo obtožuje, zamujeno kaznuje.', 'Kdor gre na Dunaj, naj pusti trebuh zunaj.', 'Počasi se daleč pride, naglica koristi samo zajcem.']

# prints out synonyms and translations of Slovenian proverbs

for proverb in proverbs:
  print("{0:>12s} | '{1:s}'".format('Proverb', proverb))
  print("{0:>12s} | '{1:s}'".format('Synonym', re.sub(r'[a-zčšžA-ZČŠŽ]+', synonym, proverb)))
  print("{0:>12s} | '{1:s}'".format('HR', translate(proverb, 'hr')))
  print("{0:>12s} | '{1:s}'".format('EN', translate(proverb)))
  print("{0:>12s} | '{1:s}'".format('DE', translate(proverb, 'de')))
  print("{0:>12s} | '{1:s}'".format('FR', translate(proverb, 'fr')))
  print("{0:>12s} | '{1:s}'\n".format('ZH', translate(proverb, 'zh-CN')))

print("{0:>12s} | {1:.1f} sec\n".format('Time', time() - start))

#!/usr/bin/python
# coding=utf8

import httplib
import re

# establishes a connection to faculty schedule at 'https://urnik.fmf.uni-lj.si'

conn = httplib.HTTPSConnection('urnik.fmf.uni-lj.si')

# creates a request for schedule of 2nd year students of program 'Praktična matematika'

conn.request('GET', '/letnik/44')

# parses names of courses including all lectures and labs included in the schedule

courses = []
for course in re.findall(r'<a href="/predmet/\d+">[^<]+</a>', conn.getresponse().read()):
  courses.append(re.sub(r'^\s+', '', re.split('\n', course)[1]))

# prints out unique names of courses included in the schedule

for i, course in enumerate(set(courses)):
  print("   {0:d}. {1:s}".format(i + 1, course))

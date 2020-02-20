import http.client
import re

# establishes a connection to faculty schedule at 'https://urnik.fmf.uni-lj.si'

conn = http.client.HTTPSConnection('urnik.fmf.uni-lj.si')

# creates a request for the schedule of 2nd year students of 'Praktična matematika'

conn.request('GET', '/letnik/44/')

# parses names of courses including all lectures and labs in the schedule

courses = set()
for course in re.findall(r'<a href="/predmet/\d+/">[^<]+</a>', conn.getresponse().read().decode()):
  courses.add(re.sub(r'^\s+', '', re.split('\n', course)[1]))

# prints out unique names of courses included in the schedule

for i, course in enumerate(sorted(courses)):
  print("{0:2d}. {1:s}".format(i + 1, course))

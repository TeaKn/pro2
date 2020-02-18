"""
p1.1 - Lists and Looney Tunes
"""

loonies = ['Conrad the Cat', 'Bosko', 'Slowpoke Rodriguez', 'Miss Prissy', 'Elmer Fudd', 'Daffy Duck', 'K-9', 'Cool Cat', 'Bugs Bunny', 'Goopy Geer', 'Inki', 'Quick Brown Fox and Rapid Rabbit', 'Petunia Pig', 'Egghead Jr.', 'Penelope Pussycat', 'Foxy', 'Hippety Hopper', 'Hector the Bulldog', 'Cecil Turtle', 'Yosemite Sam', 'Beaky Buzzard', 'Merlin the Magic Mouse', 'Colonel Shuffle', 'Lola Bunny', 'Goofy Gophers', 'Babbit, Catstello', 'The Three Bears', 'Barnyard Dawg', 'Witch Hazel', 'Blacque Jacque Shellacque', 'Henery Hawk', 'Charlie Dog', 'Sylvester Jr.', 'Melissa Duck', 'Playboy Penguin', 'Porky Pig', 'Buddy', 'Honey Bunny', 'Wile E. Coyote', 'Clyde Bunny', 'Granny', 'Tasmanian Devil', 'Gabby Goat', 'Marvin the Martian', 'Count Blood Count', 'Road Runner', 'Sylvester', 'Marc Antony and Pussyfoot', 'Pep Le Pew', 'Rocky and Mugsy', 'Beans', 'Hubie and Bertie', 'Michigan J. Frog', 'Sniffles', 'Speedy Gonzales', 'Willoughby the Dog', 'Piggy', 'Nasty Canasta', 'Sam Sheepdog', 'Hugo the Abominable Snowman', 'Gossamer', 'Pete Puma', 'Foghorn Leghorn', 'Ralph Wolf', 'Spike the Bulldog and Chester the Terrier', 'Claude Cat', 'Tweety']

loonies.sort()
print(loonies[:5])
print([c for c in loonies if c.startswith('B')])

"""
p1.2 - Tuples and dog farm
"""

dogs = [('Cufi', 'M', 2012), ('Lora', 'F', 2015), ('Hera', 'F', 2009), ('Oliver', 'M', 2015), ('Bevsk', 'M', 2018), ('Maša', 'F', 2017)]

for i, (n1, g1, y1) in enumerate(dogs):
  for j, (n2, g2, y2) in enumerate(dogs):
    if i < j and g1 != g2 and abs(y1 - y2) < 3:
      print((n1, n2) if g1 == 'M' else (n2, n1))

pairs = []
for i, (n1, g1, y1) in enumerate(dogs):
  for j, (n2, g2, y2) in enumerate(dogs):
    if i not in pairs and j not in pairs and g1 != g2 and abs(y1 - y2) < 3:
      print((n1, n2) if g1 == 'M' else (n2, n1))
      pairs.extend([i, j])

"""
p1.3 - Recursive implementation of factorial
"""

def factorial(n):
  if n <= 1:
    return 1
  else:
    return n * factorial(n - 1)

print(factorial(99))

"""
p1.3 - Iterative implementation of factorial
"""

def factorial(n):
  f = 1
  while n > 1:
    f *= n
    n -= 1
  return f

print(factorial(9999))

"""
p1.3 - Recursive implementation of multifactorial
"""

def multifactorial(n, k):
  if n <= 1:
    return 1
  else:
    return n * multifactorial(n - k, k)

print(multifactorial(999, 11))

"""
p1.3 - Iterative implementation of multifactorial
"""

def multifactorial(n, k):
  f = 1
  while n > 1:
    f *= n
    n -= k
  return f

print(multifactorial(99999, 11))

"""
p1.4 - Implementation of hashtag counting
"""

def hashtags(s):
  i = 1
  t = ''
  for c in s:
    if c == '#':
      t += str(i)
      i += 1
    else:
      t += c
  print(t)

hashtags('a# b# ### -#-##- (#,#) xy # ##')

"""
p1.4 - Implementation of hashtag sequencing
"""

def hashseqs(s):
  i = 0
  t = ''
  for c in s:
    if c == '#':
      i += 1
    elif i > 0:
      t += str(i) + c
      i = 0
    else:
      t += c
  if i > 0:
    t += str(i)
  print(t)

hashseqs('a# b# ### -#-##- (#,#) xy # ##')

"""
p1.5 - Dictionaries and Google Translate
"""

sl_en = {'seks': 'sex', 'ti': 'you', 'nerodno': 'akward', 'well': 'good', 'delati': 'make', 'peči': 'bake', 'torta': 'cake', 'drugo': 'other'}
en_de = {'sex': 'Sex', 'you': 'Sie', 'akward': 'peinlich', 'good': 'gut', 'make': 'machen', 'bake': 'backen', 'cake': 'Torte', 'candy': 'Sussigkeiten'}

def dictionary(x_y, y_z):
  x_z = {}
  for x in x_y:
    if x_y[x] in y_z:
      x_z[x] = y_z[x_y[x]]
  return x_z

print(dictionary(sl_en, en_de))

def translate(s, x_y, y_z):
  x_z = dictionary(x_y, y_z)
  s = s.lower()
  t = ''
  for k in s.split():
    if k in x_z:
      t += x_z[k] + ' '
    else:
      t += k + ' '
  return t

print(translate('Ti nerodno peči torta :)', sl_en, en_de))

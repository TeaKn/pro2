from calendar import *
from datetime import *
import os

"""
p3.1 - Computing with integers and fractions
"""

class NumeratorException(Exception):
  def __init__(self):
    super().__init__("numerator must be an integer or zero")

class DenominatorException(Exception):
  def __init__(self):
    super().__init__("denominator must be a non-zero integer")

class InvalidFractionException(Exception):
  def __init__(self, string):
    super().__init__("'{0:s}' is not a valid fraction".format(string))

class InvalidIntegerException(Exception):
  def __init__(self, string):
    super().__init__("'{0:s}' is not a valid integer".format(string))

class Fraction:
  def __init__(self, numerator, denominator = 1):
    if not isinstance(numerator, int):
      raise NumeratorException()
    if not isinstance(denominator, int) or denominator == 0:
      raise DenominatorException()
    self.numerator = numerator
    self.denominator = denominator
    self.reduce()
    
  def __repr__(self):
    if self.denominator == 1:
      return "Fraction({0:d})".format(self.numerator)
    return "Fraction({0:d}, {1:d})".format(self.numerator, self.denominator)

  def __str__(self):
    if self.denominator == 1:
      return "{0:d}".format(self.numerator)
    return "{0:d}/{1:d}".format(self.numerator, self.denominator)

  def __add__(self, fraction):
    return Fraction(self.numerator * fraction.denominator + self.denominator * fraction.numerator, self.denominator * fraction.denominator)

  def __sub__(self, fraction):
    return Fraction(self.numerator * fraction.denominator - self.denominator * fraction.numerator, self.denominator * fraction.denominator)

  def __mul__(self, fraction):
    return Fraction(self.numerator * fraction.numerator, self.denominator * fraction.denominator)

  def __div__(self, fraction):
    return Fraction(self.numerator * fraction.denominator, self.denominator * fraction.numerator)

  def add(self, fraction):
    self.numerator, self.denominator = self.numerator * fraction.denominator + self.denominator * fraction.numerator, self.denominator * fraction.denominator
    self.reduce()

  def subtract(self, fraction):
    self.numerator, self.denominator = self.numerator * fraction.denominator - self.denominator * fraction.numerator, self.denominator * fraction.denominator
    self.reduce()

  def multiply(self, fraction):
    self.numerator, self.denominator = self.numerator * fraction.numerator, self.denominator * fraction.denominator
    self.reduce()

  def divide(self, fraction):
    if fraction.numerator == 0:
      raise DenominatorException()
    self.numerator, self.denominator = self.numerator * fraction.denominator, self.denominator * fraction.numerator
    self.reduce()

  def reduce(self):
    if self.denominator < 0:
      self.numerator, self.denominator = -self.numerator, -self.denominator
    gcd = Fraction.gcd(self.numerator, self.denominator)
    self.numerator //= gcd
    self.denominator //= gcd

  @staticmethod
  def parse(string):
    try:
      numbers = string.split('/')
      if len(numbers) == 1:
        return Fraction(int(numbers[0]))
      elif len(numbers) == 2:
        return Fraction(int(numbers[0]), int(numbers[1]))
      else:
        raise Exception()
    except Exception:
      raise InvalidFractionException(string)

  @staticmethod
  def gcd(first, second):
    if first < 0:
      return Fraction.gcd(-first, second)
    elif second == 0:
      return first
    return Fraction.gcd(second, first % second)

class Integer(Fraction):
  def __init__(self, number):
    super().__init__(number)

  def __repr__(self):
    return "Number({0:d})".format(self.numerator)

  def __str__(self):
    return "{0:d}".format(self.numerator)

  @staticmethod
  def parse(string):
    try:
      return Integer(int(string))
    except Exception:
      raise InvalidIntegerException(string)

with open(os.path.join('.', 'fractions.txt'), 'r') as fractions:
  with open(os.path.join('.', 'reduced.txt'), 'w') as reduced:
    for fraction in fractions:
      reduced.write("{0:s}\n".format(str(Fraction.parse(fraction))))

F = Fraction(0)
with open(os.path.join('.', 'fractions.txt'), 'r') as fractions:
  for fraction in fractions:
    F += Fraction.parse(fraction)
print(F)

F = Fraction(1)
with open(os.path.join('.', 'fractions.txt'), 'r') as fractions:
  for fraction in fractions:
    F *= Fraction.parse(fraction)
print(F)

with open(os.path.join('.', 'expressions.txt'), 'r') as expressions:
  with open(os.path.join('.', 'results.txt'), 'w') as results:
    for expression in expressions:
      values = expression.split(' ')
      F = Fraction.parse(values[0])
      for i in range(1, len(values), 2):
        if values[i] == '+':
          F.add(Fraction.parse(values[i + 1]))
        elif values[i] == '-':
          F.subtract(Fraction.parse(values[i + 1]))
        elif values[i] == '*':
          F.multiply(Fraction.parse(values[i + 1]))
        elif values[i] == '/':
          F.divide(Fraction.parse(values[i + 1]))
      results.write("{0:s} = {1:s}\n".format(expression.strip(), str(F)))

"""
p3.2 - Working and computing with dates
"""

class InvalidDateException(Exception):
  def __init__(self, string):
    super().__init__("'{0:s}' is not a valid date".format(string))

class InvalidEMSOException(Exception):
  def __init__(self, string):
    super().__init__("'{0:s}' is not a valid EMSO".format(string))

class Date:
  def __init__(self, day = None, month = None, year = None):
    now = datetime.now()
    self.day = now.day if day is None else day
    self.month = now.month if month is None else month
    self.year = now.year if year is None else year
    if not self.valid():
      raise InvalidDateException(str(self))

  def __str__(self):
    return "{0:d}.{1:d}.{2:d}".format(self.day, self.month, self.year)

  def __repr__(self):
    return "Date({0:d}, {1:d}, {2:d})".format(self.day, self.month, self.year)

  def __lt__(self, date):
    if self.year < date.year:
      return True
    elif self.year == date.year and self.month < date.month:
      return True
    elif self.year == date.year and self.month == date.month and self.day < date.day:
      return True
    return False

  def __eq__(self, date):
    return self.year == date.year and self.month == date.month and self.day == date.day

  def day_in_year(self):
    days = 0
    for month in range(1, self.month):
      days += monthrange(self.year, month)[1]
    return days + self.day

  def days_from_epoch(self):
    days = 0
    for year in range(1900, self.year):
      days += 365 + (1 if monthrange(year, 2)[1] == 29 else 0)
    return days + self.day_in_year()

  def days_between(self, date = None):
    if date is None:
      date = Date()
    return date.days_from_epoch() - self.days_from_epoch()

  def valid(self):
    if not isinstance(self.year, int) or self.year < 1900:
      return False
    elif not isinstance(self.month, int) or self.month < 1 or self.month > 12:
      return False
    elif not isinstance(self.day, int) or self.day < 1 or self.day > monthrange(self.year, self.month)[1]:
      return False
    return True

  @staticmethod
  def parse(string):
    date = string.split('.')
    if len(date) == 3:
      return Date(int(date[0]), int(date[1]), int(date[2]))
    else:
      raise InvalidDateException(string)

  @staticmethod
  def emso(string):
    try:
      return Date(int(string[:2]), int(string[2:4]), (1000 if string[4] == '9' else 2000) + int(string[4:7]))
    except:
      raise InvalidEMSOException(string)

  @staticmethod
  def dates(month, year):
    for day in range(monthrange(year, month)[1]):
      yield Date(day + 1, month, year)

D = None
with open(os.path.join('.', 'dates.txt'), 'r') as dates:
  for date in dates:
    d = Date.parse(date)
    if D is None or d < D:
      D = d
print(D)

D = []
with open(os.path.join('.', 'dates.txt'), 'r') as dates:
  for date in dates:
    D.append(Date.parse(date))

with open(os.path.join('.', 'sorts.txt'), 'w') as sorts:
  for d in sorted(D):
    sorts.write("{0:s}\n".format(str(d)))

print([d for d in Date.dates(2, 2020)])

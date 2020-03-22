import xlrd
import requests

import datetime
from math import sqrt

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

# defines desired time range of COVID-19 data

FROM = datetime.date(2020, 2, 1)
TO = datetime.date.today()

# defines relevant countries for COVID-19 data

COUNTRIES = [None, "China", "Spain", "France", "Italy", "Slovenia"]

# defines key and identificator for Google Maps API

GOOGLE_KEY = "AIzaSyAVQmL3OzqWCQWde9DGoz28qMJeQfeKkLU"
GOOGLE_ID = "007063895917883221049:q95ltmnjmvc"

# defines custom colors used for plotting

BLACK, WHITE = [0.01] * 3, [0.9] * 3
GRAY, RED = [0.33] * 3, [0.6, 0, 0]
LIGHT_GRAY = [(rgb + 1) / 2 for rgb in GRAY]
LIGHT_RED = [(2 * rgb + 1) / 3 for rgb in RED]

def retrieve_data(date = TO):
  """
  Retrieve COVID-19 cases and deaths before the specified date from ECDC web page.
  Function stores cases and deaths evolution by country to default Excel file.
  """
  try:
    with open('covid_19.xlsx', 'wb') as file:
      file.write(requests.get('https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide-' + str(date) + '.xlsx').content)
    
    xlrd.open_workbook('covid_19.xlsx')
  except:
    retrieve_data(date - datetime.timedelta(1))

def reformat_data():
  """
  Reformat COVID-19 cases and deaths data from default Excel file to TSV file.
  Function stores cases and deaths evolution by country to default TSV file.
  """
  with open('covid_19.tab', 'w') as file:
    file.write("date\tcases\tdeaths\tcountry\tcid\n")
  
    for i, row in enumerate(xlrd.open_workbook('covid_19.xlsx').sheet_by_index(0).get_rows()):
      if i > 0:
        file.write(str(datetime.date(int(row[3].value), int(row[2].value), int(row[1].value))) + "\t" + str(row[4].value) + "\t" + str(row[5].value) + "\t" + row[6].value + "\t" + row[7].value + "\n")

def read_data():
  """
  Read COVID-19 cases and deaths data from default TSV file.
  Function returns cases and deaths evolution by country as list of lists.
  """
  data = []
  with open('covid_19.tab', 'r') as file:
    for i, line in enumerate(file):
      if i > 0:
        line = line.strip().split("\t")
      
        if line[4] != "JPG11668":
          data.append([datetime.datetime.strptime(line[0], "%Y-%m-%d").date(), float(line[1]), float(line[2]), line[3], line[4]])

  return data

def by_attribute(data, attribute = 0, country = None):
  """
  Aggregate selected country's COVID-19 cases and deaths data by the specified attribute.
  Function returns a tuple of lists of aggregated attribute values, cases and deaths.
  """
  if country is not None:
    data = [instance for instance in data if instance[3] == country]

  values = sorted({instance[attribute] for instance in data})

  cases = {value: 0 for value in values}
  deaths = {value: 0 for value in values}

  for instance in data:
    cases[instance[attribute]] += instance[1]
    deaths[instance[attribute]] += instance[2]

  cases = [cases[value] for value in values]
  deaths = [deaths[value] for value in values]

  return values, cases, deaths

def by_date(data, country = None):
  """
  Aggregate selected country's COVID-19 cases and deaths data by date.
  Function returns a tuple of lists of aggregated dates, cases and deaths.
  """
  return by_attribute(data, 0, country)

def by_country(data, number = 16):
  """
  Aggregate COVID-19 cases and deaths data by the selected number of countries.
  Function returns a tuple of lists of aggregated countries, cases and deaths.
  """
  countries, cases, deaths = by_attribute(data, 4)
  deaths, cases, countries = zip(*sorted(zip(deaths, cases, countries), reverse = True))

  return (countries, cases, deaths) if number is None else (countries[:number], cases[:number], deaths[:number])

def by_geography(data):
  """
  Aggregate COVID-19 cases and deaths data by country and find geographical locations by Google Maps API.
  Function returns a tuple of lists of aggregated countries, cases, deaths, longitudes and latitudes.
  """
  countries, cases, deaths = by_country(data, None)
  addresses = {instance[4]: instance[3] for instance in data}

  longitudes, latitudes = [], []
  for country in countries:
    location = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=' + addresses[country] + '&key=' + GOOGLE_KEY).json()['results'][0]['geometry']['location']

    longitudes.append(location['lng'])
    latitudes.append(location['lat'])

  return countries, cases, deaths, longitudes, latitudes

def plot_date(data, country = None):
  """
  Plot selected country's COVID-19 cases and deaths data by date as a line plot with custom colors.
  Method stores the line plot including labels and legend to the default file in PDF format.
  """
  dates, cases, deaths = data

  fig = plt.figure()

  plt.plot(dates, cases, marker = 'o', c = GRAY, markeredgecolor = WHITE, zorder = 0, label = "Cases")
  plt.plot(dates, deaths, marker = 'o', c = RED, markeredgecolor = WHITE, zorder = 0, label = "Deaths")

  plt.plot(dates, [sum(cases[:i + 1]) for i in range(len(cases))], c = GRAY, zorder = 1)
  plt.plot(dates, [sum(deaths[:i + 1]) for i in range(len(deaths))], c = RED, zorder = 1)

  plt.yscale('log')
  plt.xlim(FROM, TO)
  plt.xticks([datetime.date.fromordinal(((4 - i) * FROM.toordinal() + i * TO.toordinal()) // 4) for i in range(5)])

  plt.title("COVID-19 evolution " + ("worldwide" if country is None else "in " + country), fontweight = 'bold')
  plt.ylabel("(Cumulative) number of cases & deaths")
  plt.xlabel("Date")
  plt.legend()
  plt.close()

  # plt.show()
  fig.savefig('covid_19_' + ('world' if country is None else country.lower()) + '.pdf', bbox_inches = 'tight')

def bar_country(data):
  """
  Plot COVID-19 cases and deaths data by country as a bar chart with custom colors.
  Method stores the bar chart including labels and legend to the default file in PDF format.
  """
  countries, cases, deaths = data

  fig = plt.figure()

  plt.bar(countries, cases, color = LIGHT_GRAY, edgecolor = BLACK, zorder = 0, label = "Cases")
  plt.bar(countries, deaths, color = LIGHT_RED, edgecolor = BLACK, zorder = 1, label = "Deaths")

  plt.yscale('log')

  plt.title("COVID-19 cases by country", fontweight = 'bold')
  plt.ylabel("Number of cases & deaths")
  plt.xlabel("Country")
  plt.legend()
  plt.close()

  # plt.show()
  fig.savefig('covid_19_bar.pdf', bbox_inches = 'tight')

def map_country(data):
  """
  Plot COVID-19 cases and deaths data by country as a 2D map with world coastlines.
  Method stores the 2D map including labels and legend to the default file in PDF format.
  """
  countries, cases, deaths, longitudes, latitudes = data

  fig = plt.figure()

  map = Basemap()
  map.drawcoastlines()
  map.fillcontinents(color = WHITE)

  for i in range(len(countries)):
    plt.scatter([longitudes[i]], [latitudes[i]], marker = 'o', s = 1.5 * sqrt(cases[i]), c = [LIGHT_GRAY], edgecolors = [BLACK], zorder = 2 * (len(countries) - 1 - i), label = "Cases" if i == 0 else None)
    plt.scatter([longitudes[i]], [latitudes[i]], marker = 'o', s = 2 * sqrt(deaths[i]), c = [LIGHT_RED], edgecolors = [WHITE], zorder = 2 * (len(countries) - 1 - i) + 1, label = "Deaths" if i == 0 else None)

  plt.title("COVID-19 cases worldwide", fontweight = 'bold')
  plt.ylabel("Country latitude")
  plt.xlabel("Country longitude")
  plt.legend(loc = 'lower left')
  plt.close()

  # plt.show()
  fig.savefig('covid_19_map.pdf', bbox_inches = 'tight')

# retrieves COVID-19 cases and deaths data from ECDC web page

retrieve_data()

# reformats COVID-19 cases and deaths data from Excel to TSV file

reformat_data()

# reads COVID-19 cases and deaths data from TSV file

data = read_data()

# plots countries' COVID-19 data and stores them as PDF line plots

for country in COUNTRIES:
  plot_date(by_date(data, country), country)

# plots COVID-19 data by country and stores it as PDF bar chart

bar_country(by_country(data))

# plots COVID-19 data by country and stores it as PDF 2D map

map_country(by_geography(data))

from Rv import *

import numpy as np
from math import exp

# defines desired history of COVID-19 data

DATA = 21

# defines desired prediction period for COVID-19

PREDICT = 14

def regression(x, y):
  """
  Compute linear regression coefficients of given data using least squares approach.
  Function returns coefficients of linear function approximating given data.
  """
  n, mx, my = len(x), np.mean(x), np.mean(y)
  k = (np.sum(x * y) - n * my * mx) / (np.sum(x * x) - n * mx * mx)
  return my - k * mx, k

# retrieves, reformats and reads COVID-19 from ECDC web page

# retrieve_data()
# reformat_data()
data = read_data()

# aggregates data by country and computes cumulative numbers

dates, cases, deaths = by_date(data)
cases = [sum(cases[:i + 1]) for i in range(len(cases))]
deaths = [sum(deaths[:i + 1]) for i in range(len(deaths))]

# reduces data to desired history and stores date limits

dates, cases, deaths = dates[-DATA:], cases[-DATA:], deaths[-DATA:]
start, end = dates[0], dates[-1] + datetime.timedelta(PREDICT)

# computes regression coefficients by fitting exponential to data

nc, kc = regression(np.array([date.toordinal() for date in dates]), np.log(cases))
nd, kd = regression(np.array([date.toordinal() for date in dates]), np.log(deaths))

# plots historical data of COVID-19 cases and deaths

fig = plt.figure()

plt.scatter(dates, cases, marker = 'o', s = 48, c = [LIGHT_GRAY], edgecolors = [BLACK], label = "Cases (data)")
plt.scatter(dates, deaths, marker = 'o', s = 48, c = [LIGHT_RED], edgecolors = [BLACK], label = "Deaths (data)")

# computes predicted values of COVID-19 cases and deaths

dates = [dates[-1] + datetime.timedelta(days + 1) for days in range(PREDICT)]
cases = [exp(kc * date.toordinal() + nc) for date in dates]
deaths = [exp(kd * date.toordinal() + nd) for date in dates]

# plots predicted values with annotations of COVID-19 cases and deaths

plt.scatter(dates, cases, marker = '*', s = 72, c = [WHITE], edgecolors = [GRAY], label = "Cases ({0:d} days)".format(PREDICT))
plt.scatter(dates, deaths, marker = '*', s = 72, c = [WHITE], edgecolors = [RED], label = "Deaths ({0:d} days)".format(PREDICT))

plt.annotate("{:,.0f} cases".format(cases[-1]), xy = (end, cases[-1]), xytext = (4, 0), textcoords = 'offset points')
plt.annotate("{:,.0f} deaths".format(deaths[-1]), xy = (end, deaths[-1]), xytext = (4, 0), textcoords = 'offset points')

# sets horizontal (and vertical) axis and constructs legend

# plt.yscale('log')
# plt.ylim(500, 10**8)
plt.xlim(start, end)
plt.xticks([datetime.date.fromordinal(((4 - i) * start.toordinal() + i * end.toordinal()) // 4) for i in range(5)])
plt.legend(loc = 'upper left')

# sets figure title and labels of axes

plt.title("COVID-19 evolution prediction", fontweight = 'bold')
plt.ylabel("Cumulative number of cases & deaths")
plt.xlabel("Date")
plt.close()

# stores figure as PDF line plot

fig.savefig('covid-19.pdf', bbox_inches = 'tight')

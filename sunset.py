#!/usr/bin/env python

import datetime
import ephem
import random


LATITUDE       = '49.245862'
LONGITUDE      = '-123.106073'
ELEVATION      = 30 #in meters
TIME_RAND_LOW  = 5 #random minutes lower limit
TIME_RAND_HIGH = 35 #random minutes upper lmiit


def check():
  location  = ephem.Observer()
  location.lat  = LATITUDE
  location.long = LONGITUDE
  location.elev = ELEVATION

  sun = ephem.Sun()
  sun.compute()

  # calculate today's sunset
  sunset  = ephem.localtime(location.next_setting(sun))
  # add delta to sunset
  sunset_delta   = sunset + datetime.timedelta(minutes = random.randint(TIME_RAND_LOW,TIME_RAND_HIGH))
  # get current date/time
  current = datetime.datetime.now()

  if (current.hour == sunset_delta.hour) and (current.minute > sunset_delta.minute):
    return "down"

  elif (current.hour > sunset_delta.hour):
    return "down"

  else:
    return "up"


if __name__ == "__main__":
    check()

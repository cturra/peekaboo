#!/usr/bin/env python

import ConfigParser
import datetime
import ephem
import os
import sys
import random

CONFIG_FILE = os.path.dirname(__file__)+'/config/settings.cfg'

def read_config(SECTION, ATTRIBUTE):
  if os.path.isfile(CONFIG_FILE):
    config = ConfigParser.RawConfigParser()
    config.read(CONFIG_FILE)

    try:
      return config.get(SECTION, ATTRIBUTE)  

    except:
      print "CONFIG: Could not read "+SECTION+" and "+ATTIRUBTE+" from ("+CONFIG_FILE+")."
      sys.exit(1)

  else:
    print "CONFIG: file ("+CONFIG_FILE+") is not found."
    sys.exit(1)


def check():
  location  = ephem.Observer()
  location.lat  = read_config('SUN', 'latitude')
  location.long = read_config('SUN', 'longitude')
  location.elev = int(read_config('SUN', 'elevation'))

  sun = ephem.Sun()
  sun.compute()

  TIME_RAND_LOW  = int(read_config('DELTA', 'low')) #random minutes lower limit
  TIME_RAND_HIGH = int(read_config('DELTA', 'high')) #random minutes upper lmiit

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

#!/usr/bin/env python

from ouimeaux.environment import Environment
import sunset
import sys
import time

DEBUG = False

## --- the good stuff hapens below this ---
def main():
  WEMO_ACTION = sys.argv[1]

  env = Environment()
  env.start()

  if (WEMO_ACTION.lower() != 'list'):
    WEMO_DEVICE = sys.argv[2]
    # make sure we can actually connect to device
    try:
      switch = env.get_switch(WEMO_DEVICE)
    except:
      try:
        # will return UnknownDevice exception if discover has not been
        # run. lets try that first before assuming the device is wrong.
        env.discover(seconds=3)
        switch = env.get_switch(WEMO_DEVICE)
      except:
        print "Failed to connect to wemo device: "+WEMO_DEVICE
        sys.exit(1)

  # return a list of the switch devices
  if WEMO_ACTION.lower() == 'list':
    if DEBUG: print "Action: listing all wemo switch devices."
    switches = env.list_switches()
    if (len(switches) > 0):
      print "The following WeMo switches were found:"
      for switch in switches:
        print " -> "+switch

  # force the switch off
  elif WEMO_ACTION.lower() == 'off':
    if DEBUG: print "Action: shut off wemo device."
    switch.off()

  # force the switch on
  elif WEMO_ACTION.lower() == 'on':
    if DEBUG: print "Action: tun on wemo device."
    switch.on()

  # wait for sunset, then turn switch on
  elif WEMO_ACTION.lower() == 'sunset':
    if DEBUG: print "Action: check sunset."

    # check if the sun is down and the switch state is off (0)
    while(switch.get_state() == 0):
      if sunset.check() == 'down':
        if DEBUG: print " => sun has set, turning the switch on."
        switch.on()

      else:  
        time.sleep(300) # sleep for 5 minutes

  # return the current switch state
  elif WEMO_ACTION.lower() == 'status':
    if DEBUG: print "Action: check state."
    state = switch.get_state()

    if state > 0:
      print "Device ("+WEMO_DEVICE+"): On."

    else:
      print "Device ("+WEMO_DEVICE+"): Off."

  # unknown action. return error
  else:
    print "Action: Invalid action provided."
    sys.exit(1)


# print usage
def usage():
  print "Usage: "+sys.argv[0]+" <action> [wemo_switch]"
  print " - action: list, off, on, status, sunset, status"
  print " - wemo_switch: switch name. not required for list."


if __name__ == "__main__":
  if len(sys.argv) < 3:
    if len(sys.argv) == 2 and sys.argv[1] == 'list':
      main()
    else:
      usage()
      sys.exit(1)

  else:
    main()

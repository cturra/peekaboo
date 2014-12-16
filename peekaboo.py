#!/usr/bin/env python

from ouimeaux.environment import Environment
import argparse
import sunset
import sys
import time

## --- the good stuff hapens below this ---

def get_switch(env, WEMO_DEVICE):
  # make sure we can actually connect to device
  try:
    return env.get_switch(WEMO_DEVICE)
  except:
    try:
      # will return UnknownDevice exception if discover has not been
      # run. lets try that first before assuming the device is wrong.
      env.discover(seconds=3)
      return env.get_switch(WEMO_DEVICE)
    except:
      print "Failed to connect to wemo device: "+WEMO_DEVICE
      sys.exit(1)


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Belkin WeMo device control.')
  parser.add_argument('action', type=str,
                      help='action to pass WeMo device. Available actions: list, off, on, status, sunset.')
  parser.add_argument('-d', '--device', type=str, nargs=1,
                      help='WeMo device.')
  parser.add_argument('-v', '--verbose', help='execute in VERBOSE mode', action='store_true')
  args = parser.parse_args()

  if args.action != 'list' and args.device is None:
    parser.error("--device is needed for "+args.action)
  elif args.action != 'list' and args.device is not None:
    WEMO_DEVICE = args.device[0]

  WEMO_ACTION = args.action
  VERBOSE     = args.verbose

  env = Environment(with_cache=False)
  env.start()

  # return a list of the switch devices
  if WEMO_ACTION.lower() == 'list':
    if VERBOSE: print "Action: listing all wemo switch devices."
    # first, run a discover in case there are new devices on the network
    env.discover(seconds=3)
    # now get a list of switches
    switches = env.list_switches()
    if (len(switches) > 0):
      print "The following WeMo switches were found:"
      for switch in switches:
        print " -> "+switch

  # force the switch off
  elif WEMO_ACTION.lower() == 'off':
    if VERBOSE: print "Action: shut off device: "+WEMO_DEVICE
    switch = get_switch(env, WEMO_DEVICE)
    switch.off()

  # force the switch on
  elif WEMO_ACTION.lower() == 'on':
    if VERBOSE: print "Action: tun on device: "+WEMO_DEVICE
    switch = get_switch(env, WEMO_DEVICE)
    switch.on()

  # wait for sunset, then turn switch on
  elif WEMO_ACTION.lower() == 'sunset':
    if VERBOSE: print "Action: check sunset."

    switch = get_switch(env, WEMO_DEVICE)
    # check if the sun is down and the switch state is off (0)
    while(switch.get_state() == 0):
      if sunset.check() == 'down':
        if VERBOSE: print " => sun has set, turning the switch on."
        switch.on()

      else:  
        time.sleep(300) # sleep for 5 minutes

  # return the current switch state
  elif WEMO_ACTION.lower() == 'status':
    if VERBOSE: print "Action: check state."
    switch = get_switch(env, WEMO_DEVICE)
    state = switch.get_state()

    if state > 0:
      print "Device ("+WEMO_DEVICE+"): On."

    else:
      print "Device ("+WEMO_DEVICE+"): Off."

  # unknown action. return error
  else:
    print "Action: Invalid action provided."
    sys.exit(1)

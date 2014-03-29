#Peekaboo: Belkin WeMo Device control

The Peekaboo project was created to interface with the [ouimeaux project](https://github.com/iancmcc/ouimeaux)
to control the [Belkin WeMo](http://www.belkin.com/us/Products/home-automation/c/wemo-home-automation) devices in 
my house. Currently, it's being used with cron as the scheduler to turn on my front lights around sunset (with a 
time delta) and off later in the evening.



##Installation

###Debian/Ubuntu
You will need a couple python packages installed before you can complete the Peekaboo installation. Before moving
on, run the following:

```
  $ sudo apt-get install python-setuptools python-dev python-pip
```

After you have cloned this repo, you will also need to install [PyEphem](http://rhodesmill.org/pyephem/) and
[ouimeaux](https://github.com/iancmcc/ouimeaux). Here is a quick and dirty example of how you can get this 
installed, tho, there are several other methods:

```
  $ git clone https://github.com/cturra/peekaboo
  $ pip install -r peekaboo/requirements.txt
```


##Example run

```
  $ python peekaboo.py list
  The following WeMo switches were found:
   -> Front Lights

  $ python peekaboo.py status "Front Lights"
  Device (Front Lights): Off.
```


##Setting up a cron

The following cron example, is what I am using to have peekaboo check when the sun has set and turn on the lights
for me. Then, later in the evening, I have peekaboo shut the lights off for me.

```
  # check for sunset to turn on front lights
  20 16 * * * python /home/cturra/peekaboo/peekaboo.py sunset "Front Lights"

  # turn the lights off for the night
  30 23 * * * python /home/cturra/peekaboo/peekaboo.py off "Front Lights"
```

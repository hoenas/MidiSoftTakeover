'''
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''



import time
import rtmidi

# open config file
lineCounter = 0
with open("config.txt") as file:
    line = file.readline()
    line = line.replace("\n", "")
    device_name = line
    line = file.readline()
    line = line.replace("\n", "")
    virtual_device_name = line

momentumFactor = 0.4
minThreshold = 10

# variables
inputPort = None
outputPort = None

# search for input device
print "Searching input port..."
for port in rtmidi.MidiIn().get_ports():
    print " -", port, ":",
    if(port  == device_name):
        inputPort = port
        print "match!"
        break
    else:
        print "no match..."

# exit, if device was not found
if inputPort == None:
    print "Input device", device_name, "not found!"
    exit()

# search for output device
print "Searching output port..."
for port in rtmidi.MidiOut().get_ports():
    print " -", port, ":",
    if (port == virtual_device_name):
        outputPort = port
        print "match!"
        break
    else:
        print "no match..."

# exit if device not found
if outputPort == None:
    print "Output device", device_name, "not found!"
    exit()

# dict with old midi-values:
oldValues = {}

# Callback for incoming messages
def callback(message, time_stamp):
    channel = message[0][0]
    # ignore non continous control change messages
    if channel & 0xF0 == 0xB0:
        # continue
        control = message[0][1]
        value = message[0][2]

        try:
            # check for threshold
            if oldValues[channel][control][0] == value:
                # send message through virtual midi port
                midi_out.send_message([channel, control, value])
                # put current value to oldValues
                oldValues[channel][control] = (value, time.time())
            elif oldValues[channel][control][0] > value:
                if (oldValues[channel][control][0] - value) <= (minThreshold + momentumFactor / (time.time() - oldValues[channel][control][1])):
                    #print message, "released"
                    # send message through virtual midi port
                    midi_out.send_message([channel, control, value])
                    # put current value to oldValues
                    oldValues[channel][control] = (value, time.time())
                #else:
                #    print message, "locked", (minThreshold + momentumFactor / (time.time() - oldValues[channel][control][1]))
            elif oldValues[channel][control][0] < value:
                if (value - oldValues[channel][control][0]) <= (minThreshold + momentumFactor / (time.time() - oldValues[channel][control][1])):
                    #print message, "released"
                    # send message through virtual midi port
                    midi_out.send_message([channel, control, value])
                    # put current value to oldValues
                    oldValues[channel][control] = (value, time.time())
                #else:
                #    print message, "locked", (minThreshold + momentumFactor / (time.time() - oldValues[channel][control][1]))



        except:
            # add control to dictionary
            print "new control discovered, channel:", channel & 0x0F, "control:", control
            if channel not in oldValues:
                oldValues[channel] = {control : (value, time.time())}
            elif control not in oldValues[channel]:
                oldValues[channel][control] = (value, time.time())
            # send message through virtual midi port
            midi_out.send_message([channel, control, value])


print "Opening ports...",
# listen for incomming messages and check midi softtakeover
midi_in = rtmidi.MidiIn()
midi_in.set_callback(callback)
midi_in.open_port(int(inputPort[-1]))

midi_out = rtmidi.MidiOut()
midi_out.open_port(int(outputPort[-1]))


print "ok."
print "=== SOFT TAKEOVER READY ==="

# dont exit
while(True):
    pass

del midi_in
del midi_out

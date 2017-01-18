# MidiSoftTakeover
A simple script which allows midi soft takeover for DAWs that do not support it. Requires a virtual midi port.

HOWTO:
- Download and install a virtual midi driver (I used loopMIDI by Tobias Erichsen, http://www.tobias-erichsen.de/software/loopmidi.html)
- Add a virtual midi port (I used nanoKONTROL Soft Takeover)
- Edit the file config.txt:
- first line is the name of your input device (in my case "nanoKONTROL 0", whereas the 0 at the end seems to be the port index)
- second line is the name of your output device, you put your created virtual midi port here ("nanoKontrol Soft Takeover 2" in my case, again, the number seems to be the port index)
- run the script
- run DAW
- enable the virtual midi port (not the real device!)

This is a basic script that I use to start a new Mobiflight Custom device. I start a lot and finish a few of these, so this script is really handy.

Usage:
cd to parent folder.
run the setup_device.bat script. Usage:
    setup_device.bat <device_name> <prefix>

e.g. setup_device.bat MyCustomDevice Mobiflight

Or, my most recent example:
setup_device.bat CC_KAP140_LCD CCrawford

NOTES:
Take a look at the batch file and run the commands separatedly if you (or your OS) are squeemish about running a .bat file. It's just a clone, a folder rename, and the a Python script.

You need Python 3 installed and on your path.
You need a few common python libraries. shutil, pathlib.

The script may be really basic in the renaming. E.g. you may want more sophistication in naming your devices, etc. 
You still need to go in and manually edit things like websites, descriptions, hardware config, etc. This merely renames things in the boilerplate so you can get going.

Feedback 100% welcome. This is a v0.1

--Chris

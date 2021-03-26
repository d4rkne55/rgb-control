# rgb-control

So, after I added an RGB LED strip to my PC I wanted to control it of course.
I saw that MSI, for my B450 mainboard, wants me to install a software suite
full of stuff I don't care about, with over 400 MiB basically bloatware - the MSI Dragon Center.
It did also list Mystic Light as a stand-alone application, but it mentioned to be
for Win 7 & 8 only and seemed unsupported (also the download link didn't actually work).

I did not want that, I avoid bloatware, I wanted a lightweight application that
just does what I need.  
So I searched for alternatives, but unfortunately didn't find sth. that worked - both
[MSIRGB](https://github.com/ixjf/MSIRGB) and [OpenRGB](https://gitlab.com/CalcProgrammer1/OpenRGB)
did not work with my mainboard; the latter had support once but it has been deactivated due
to bricking risks. All led me to research more and I got pretty interested in reading
some issues from the projects. I don't know C++ (yet) though and don't have experience
in reverse engineering, but I saw one guy mentioning that he wrote sth. in Python,
trying to help the issue by finding out how his Z490 (MSI) board works.
Not knowing Python really well, but having learned the basics and been
playing around with it about a year before, I decided to try writing something
myself to control my mainboard. The issue was full of helpful information,
incl. how one could "unbrick" the board, so the risk was not that high anymore.

So, I tried running the old Mystic Light application - after working around MSIs
HTTPS Mixed-Content issue on their website that prevented the download.  
And this is what happened after having used Mystic Light and Wireshark,
doing some reverse engineering, and diving deeper into Python. :)


## Support

- MSI B450 Gaming Pro Carbon AC

That's my mainboard. Adding more support is not planned, as this is mostly
just for me - although the application is done in a way to be extendable.
I'm thinking about adding support for my Sapphire RX 5700 XT Nitro+ too, but I'll see.


## Installation

`pip install -r requirements.txt`

Requires/built on Python 3.8.


## Usage

After starting the program, it will scan for HID devices and list the supported ones.
When it found some and you selected a device, it will ask you to configure all
lighting zones. As everything is dynamic based on the device config, it's not
really user-friendly and hard to configure without knowing your device's data format.
You may check the zone config of the device for some orientation.
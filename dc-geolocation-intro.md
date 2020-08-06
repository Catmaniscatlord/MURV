
[//]: <> (you can convert this file to pdf or html with)
[//]: <> (pandoc dc-geolocation-intro.md -o dc-geolocation-intro.pdf)
[//]: <> (pandoc --mathjax dc-geolocation-intro.md -o dc-geolocation-intro.html)
[//]: <> (you can also generate any of the output formats supported)
[//]: <> (by pandoc, such as .html, .tex, and dozens of others)

Introduction
====
This paper is split into three different sections, the process of creating \
MURV, a technical overview of how MURV works, and finally what is left to be 
accomplished with MURV.


The story of MURV
=======

MURV's Goal
---

The goal of MURV is to allow for the tracking and geolocation of wireless 
devices using RSSI values.

Initial Idea
---

How the idea of MURV is not the story of trying to solve a particular
problem, but rather the story of evolving interests. During my sophomore 
year, I started messing around with hypo-cycloids and developed a little 
<a herf="https://www.desmos.com/calculator/f2owqmikqp">program</a> in an 
online graphing calculator Desmos to graph them. Following that I made 
something I liked to call the <a her="https://www.desmos.com/calculator/
6m3qvvy5kc">bi-cycloid</a>, which drew a point based on the distance to 
points rotating on two different circles. My initial idea for my project 
was to take the bi-cycloid, and expand it into the third dimension. I 
proposed this idea to my mentors they pushed the idea towards that of 
making a program that could find the location of a point in the real 
world using multitelemetry, which uses the measured distance from an unknown 
point in space to 3 or more known points in space to locate the unknown 
point. But, in order to perform multitelemetry we needed a way to get the 
distance between our unknown point and our known points. We settled on using 
RSSI values from access points(aka AP's or routers). Although this idea was 
different from what I originally wanted to accomplish I was still interested 
in it.

Early Development
-------------------

This early development was meant to get my head wrapped around 
multitelemetry and ideas and concepts behind it. What I Initialy developed 
was a crude form of multitelemetry that relied on exact distance values to 
find an exact solution. This was done by pre-defining every points location, 
and measuring their exact distance to the unknowns point using the distance 
formula with both points coordinates. This allowed me to develop a 
mathematical framework to perform the necessary multitelemetry and 
understand it's concepts. Unfortunately this framework that I created would 
be way to mathematically strict to deal with the noise and error in the real 
world of measurement.

From here I decided to move on from the mathematical side of the project to the gathering of data side. One of my mentors, Jason Schaefer, lent me 4 AP's(access points) to allow me to gather some real world data, and to learn more about what steps I would need to take to get my project to be something useable in a real-world setting.

Middle to Late Development
--------------------------





MURV from a technical standpoint
===========================================


Motivation
----------

**MURV**(multilateration using RSSI values) is a program that allows a wireless networking
device to find its own location using the information it can gather
from its network access points. This can be any device that is capable
of performing wireless networking ie. mobile phones and laptops.

Self-location can be used for several important tasks. These tasks
include locating someone in an emergency, navigation within small
areas (think of something like GPS for an apartment building), or
tracking of that device.

The only data self-location needs is the location of 4 known points
along with their distance to the unknown point. From there, what's
necessary is the mathematical framework to convert that data into our
physical location. To collect this data we obtain the information
using wireless network access points (AP's).

This project has produced two things

* A program that collects the "signal strength" from each access
  point, also known as the RSSI value.
* The mathematical framework that turns the needed data into our
  location through the process of multilateration, with a python
  program to accompanies it.

dc-geolocation is written by David Chamberlain
[catmanisacatlord@gmail.com](mailto:catmanisacatlord@gmail.com) of
Santa Fe High School and the Institute for Computing in Research.


Accessing information in a wireless access point
------------------------------------------------

Most people are only familiar with their access point from the
web-based administrative interface that they use to set it up, but one
can also use instructions to automatically get specific information
from them.

To get a feeling for how this works, try the following at the command
line of a GNU/Linux system:

<code>sudo iw dev wlp1s0 link</code>

This command will give you some basic information about the wireless
network you are currently connected to, while While this command will
give you all of the information about all of the networks in your
area:

<code>sudo iw dev wlp1s0 scan</code>

We use the second command in our program due to this functionality and
then filter away the networks and data we do not want. This leaves us
with the RSSI value along with the SSID for the AP's that we
desire. Using the Free-space path loss formula (which determines how a
signal gets quieter as it passes through free space) and rearranging
it, we can achieve a distance in meters using the formula below.

<!-- <img src="https://render.githubusercontent.com/render/math?math=\text{ distance}(\text{meters}) = 10 ^{((27.55 - {(20 \times \log_{10}(\text{ frequency}(\text{ Mhz})))} - \text{ signalLevel})/20)}"> -->

${\rm distance}({\rm meters}) = 10 ^{((27.55 - (20 \times
\log_{10}({\rm frequency}({\rm Mhz}))) + {\rm signalLevel})/20)}$

Unfortunately, a big problem with using the signal strength with
routers is how messy and scattered the signal can be, if you have that
1 wifi dead zone in your house you will understand what I mean. To get
the most accurate data it's best to use it in situations where direct
LOS(line of sight) is established between the AP and whichever
wireless device is being tracked. Ontop of this, using a 5200 MHz
frequency can hopefully reduce any noise.


The mathematics of geolocation
------------------------------

In order to calculate the unknown position of a point (ex, ey, ez), we
must have 4 known points with known locations in 3D space (an_x, an_y,
an_z) along with their distance to our unknown point
(e_a1,e_a2,e_a3,e_a4). From there we estimate the point (ex,ey,ez) so
that the difference in the distance from the estimated point to each
AP and the measured distance is minimized according to the least means
square algorithm.

In my setup I placed each of my 4 AP's on each vertex 1 meter
square with my laptop in the middle as the wireless device. This shape
was chosen due to its ease in marking the location of the AP's. I collected data in this setup and saved it in TestValues.csv, the names at the top of the file reference to the SSID values of each AP. The
diagram below depicts this, with the black circles representing AP's
and the red circle depicting the laptop. All units are in meters.


<!-- <img src="layout.png" width="200"> -->

![Layout of the receivers](layout.png "layout of the receivers"){ width=200px }


How to run the software
-----------------------

1. Download and install python 3.8.
2. Extract the name.zip file to a directory of your choosing.
3. From your terminal run <code>pip install matplotlib numpy
   pandas</code> . This will install the necessary python packages.
   
   Next, make sure that the command <code>sudo iw dev wlp1s0
   scan</code> can run without needing a password.
4. In a new terminal run <code>sudo visudo</code> . This will allow you to
   edit your sudoers file (the file that delegates permissions for
   your device) using the nano text editor.
5. Navigate to the end of the text file and type in <code>Username
   ALL=NOPASSWD: /sbin/iw</code> , for example, <code>david
   ALL=NOPASSWD: /sbin/iw</code>
6. Press ctrl+x to exit the file, next press y to save the modified
   buffer, then press enter. 
   
   NOTE: This should bring you back to your
   terminal. If the terminal says you have any syntax errors, press
   'x'. This will cancel all the changes you made to the sudoers
   file. You will need to restart the process at step 4.
7. Open up RSSIValues.py in the editor of your choice and edit the
   NETWORKS variable to the SSID values (the name of it) of the
   AP's(access points aka routers) you have.
8. Set the FREQUENCY variable to the bandwidth you are using for your
   AP's to communicate.
9. Now you finally run the program in a terminal using "python3
   pathToFile/RSSIValues.py"

Further expansion
-- 

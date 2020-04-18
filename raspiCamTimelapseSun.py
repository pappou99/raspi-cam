#!/usr/bin/python3
#  Created by James Moore on 28/07/2013.
#  Copyright (c) 2013 Fotosyn. All rights reserved.
#  Modified by Björn Bruch
#
#  Raspberry Pi is a trademark of the Raspberry Pi Foundation.

#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are met:

#  1. Redistributions of source code must retain the above copyright notice, this
#  list of conditions and the following disclaimer.
#  2. Redistributions in binary form must reproduce the above copyright notice,
#  this list of conditions and the following disclaimer in the documentation
#  and/or other materials provided with the distribution.>

#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#  DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
#  ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#  (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
#  ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

#  The views and conclusions contained in the software and documentation are those
#  of the authors and should not be interpreted as representing official policies,
#  either expressed or implied, of the FreeBSD Project.

# This script sets up and runs a Python Script which, at intervals invokes a capture 
# command to the Raspberry Pi camera, and stores those files locally in a dynamically
# named folder.

# To invoke, copy this script to an easy to find file location on your Raspberry Pi
# (eg. /home/pi/), log into your Raspberry Pi via terminal and type:
#
# sudo python /your/file/location/raspiLapseCam.py (add &) if you wish to run as a
# background task. A process ID will be shown which can be ended with

# sudo kill XXXX (XXXX = process number)

# Based on your settings the application will no begin capturing images
# saving them to your chose file location (same as current location of this file as default.
import os
import time
import math
import sonnenaufgang
import RPi.GPIO as GPIO
from datetime import datetime
import subprocess

# Set the initial serial for saved images to 1
#fileSerial = 1

# Define the root Folder where to save the images to
folder = "./timelapse/project/project_"

# Define the interval between the images in seconds
interval = 600

# Define the size of the image you wish to capture. 
imgWidth = 2592 #1920 # Max = 2592 
imgHeight = 1944 #1080 # Max = 1944

# Define the Sharpnes of the image here (values from -100 to 100)
sh = "100"

# Define the white balance mode here
awb = "sun"

# Define the exposure here
ex = "auto"

# Define the ISO here (values from 100 to 800)
iso = "100"

# Defines the position the timelapse was made (in the Format degrees/1,minutes/1,seconds/100)
gps_lat = '48/1,8/1,14/100'
gps_lon = '11/1,34/1,31/100' # example shows Marienplatz in Munich at 48°8'14''N; 11°34'31''E

while 1 == 1:
    lt = time.localtime() # Aktuelle, lokale Zeit als Tupel
    # Entpacken des Tupels
    lt_jahr, lt_monat, lt_tag = lt[0:3]        # Datum
    lt_dst = lt[8]                             # Sommerzeit
    
    #print
    #print("Heute ist der {0:02d}.{1:02d}.{2:4d}".
    #    format(lt_tag, lt_monat, lt_jahr))
    #if lt_dst == 1:
#        print("Sommerzeit")
#    elif lt_dst == 0:
#        print("Winterzeit")
#    else:
#        print("Keine Sommerzeitinformation vorhanden")

    AM, UM = sonnenaufgang.Sonnenauf_untergang (sonnenaufgang.JulianischesDatum(lt_jahr, lt_monat, lt_tag, 12, 0, 0), lt_dst + 1)

    AMh = int(math.floor(AM))
    AMm = int((AM - AMh)*60)

    UMh = int(math.floor(UM))
    UMm = int((UM - UMh)*60)

#    print("Sonnenaufgang {0:02d}:{1:02d} Sonnenuntergang {2:02d}:{3:02d}".
#      format(AMh, AMm, UMh, UMm))


    jetzt = int("{0:02d}{1:02d}".format(lt[3],lt[4]))
    auf = int("{0:02d}{1:02d}".format(AMh,AMm))
    unter = int("{0:02d}{1:02d}".format(UMh,UMm))
 
    if jetzt > auf and jetzt < unter:
        
        d = datetime.now()
        # Grab the current datetime which will be used to generate dynamic folder names
        year = "%04d" % (d.year) 
        month = "%02d" % (d.month) 
        date = "%02d" % (d.day)
        hour = "%02d" % (d.hour)
        mins = "%02d" % (d.minute)
    #if d.hour > 2:
        
        # Define the location where you wish to save files. Set to HOME as default. 
        # If you run a local web server on Apache you could set this to /var/www/ to make them 
        # accessible via web browser.
        folderToSave = str(folder) + str(year) + '-' + str(month) + '-' + str(date)
        
        os.makedirs(folderToSave, exist_ok=True)
        
        # Set FileSerialNumber to 000X using four digits
        #fileSerialNumber = "%04d" % (fileSerial)
        
        meldung_status = " ====================================== Saving file at " + hour + ":" + mins
        print(meldung_status)


        
        # Capture the image using raspistill. Set to capture with added sharpening, auto white balance and average metering mode
        # Change these settings where you see fit and to suit the conditions you are using the camera in
        cmd = "raspistill -w " + str(imgWidth) + " -h " + str(imgHeight) + " -o " + str(folderToSave) + "/" + str(year) + "-" + str(month) + "-" + str(date) + "_" + str(hour) + str(mins) +  ".jpg  -ISO " + str(iso) + " -sh " + str(sh) + " -ex " + str(ex) + " -awb " + str(awb) + " -r -q 100 --exif GPS.GPSLatitude=" + gps_lat + " --exif GPS.GPSLongitude=" + gps_lon
        pid = subprocess.call(cmd, shell=True)

        # Increment the fileSerial
        #fileSerial += 1
        
        # Wait ## seconds before next capture
        time.sleep(interval)
        
    else:
        print ("dunkel")
        time.sleep(60)

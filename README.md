						   WE SHOWED UP!!!!!!
									
Step 1: Installation of Raspbian on 16 GB (preferred) SD card:
			Download and Extract Raspbian Stretch for desktop zip from( https://www.raspberrypi.org/downloads/raspbian/ )
			Download and Install Win32 Disk Imager from (https://sourceforge.net/projects/win32diskimager/) to burn the Raspbian OS onto SD card
			Open Win32 DI -> Browse -> Select the image raspbian stretch -> Write -> Yes

Step 2: Insert the card in RPi and power it up (5v DC)

Step 3: Preferences -> Rpi Configuration -> Localisation -> Set Locale (Country to India), Timezone (Area to Indian and Location to Maldives), Keyboard (Country to India and Variant to English(India with rupee)), Wifi country (India) -> Ok -> Yes to Reboot

Step 4: Connect to the wifi

Step 5: Go to Preferences -> RPi Configuration -> Interfaces -> Enable all -> Reboot

Step 6: Downloading all the required libraries:
			Open Terminal:
				$ sudo apt-get update
				$ sudo apt-get upgrade
				
			For pi camera library:
				$ sudo apt-get install python-picamera
				
			For gps and accelerometer:
			
				BerryGPS uses the serial port on the Raspberry Pi. By default, the serial port is already assigned to the console. This can be confirmed by using
					$ dmesg | grep tty
						The last line above shows that the console is enabled for the serial port.
					$ ls -l /dev/serial0
					
				The serial console needs to be disabled and then the serial port enabled.		
					$ sudo raspi-config
					Select interfacing options -> Serial -> No -> Yes
					And then Yes to reboot
						
				To check if the gps modules is connected:
					$ i2cdetect -y 1
				
				Viewing meaningful GPS data:
					$ sudo apt-get install gpsd-clients gpsd -y
					$ sudo nano /etc/default/gpsd
						Look for
						DEVICES=””
						and change it to
						DEVICES=”/dev/serial0″
					ctrl+x -> y -> enter
					$ sudo reboot
					
				To view data:
					$ gpsmon
					or
					$ cgps
				
				
			For conversion of image to text and compression:
				$ sudo apt-get install zlib1g-dev
				$ sudo apt-get install python3-pip
				$ sudo apt-get install python-pip
				$ sudo pip3 install pybase64
			
			For firebase:
				$ sudo pip install requests==2.12.4
				$ sudo pip install python-firebase
			

Step 6: Download the source code:
			Terminal -> $ git clone https://github.com/Ankita46/GPS_ACCELEROMETER_CAM_PI.git

Step 7: Open GPS_ACCELEROMETER_CAM_PI from File Manager. Cut The LOG folder and Paste it inside Documents
		Create a folder inside LOG and name it "accel"
		Create a folder inside LOG and name it "images"

Step 8: To run the program:
			Terminal -> $ cd Documents/LOG 
			$ sudo python gpsdData.py
			

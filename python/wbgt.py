# WBGT
#
#		reads, list and plot the WBGT data at a certain weather station
#
# mdofications
#   16-jul-2026  JM  initial version 

#-jm from datetime import datetime, timedelta, timezone
#-jm import matplotlib.pyplot as plt
#-jm import matplotlib.dates as mdates
#-jm from python.opendata import OpenDataAPI

class wbgt :

	# init
	#
	#		initialises the class
	#			- sets the default location
	#			- sets the API key
	#		  - set default start and stop dates

	#-jm def __init__(self, location = "Gilze-Rijen") :

		# set the API key and the location

	#-jm	self.apiKey = "eyJvcmciOiI1ZTU1NGUxOTI3NGE5NjAwMDEyYTNlYjEiLCJpZCI6IjBhZTg4MTI5MTAzOTQyN2FiMDVhNjM2NmNiOWQxMTE3IiwiaCI6Im11cm11cjEyOCJ9"
	#-jm	self.setLocation(location)

		# use the OpenAPIdata class

	#-jm	self.api = OpenDataAPI(dataset = "wet_bulb_globe_temperature", version = "3.0", token = self.apiKey)

		# sets the default start and stop date
		
	#-jm	tz = timezone(timedelta(hours=2))
	#-jm	self.startTime = datetime.now(tz) - timedelta(hours = 6)
	#-jm	self.endTime = datetime.now(tz)

	# input
	#
	#    asks the user for start and stop dates

	#-jm def input(self) :

		#-jm inputString = "begin of WBGT data : (" + self.startTime.strftime("%d-%b-%Y %H:%M") + ") > "
		#-jmanswer = input(inputString)
		#-jmif answer != "" :
		#-jm		self.startTime = datetime.strptime(answer, "%d-%b-%Y %H:%M")

		#-jminputString = "end of WBGT data : (" + self.endTime.strftime("%d-%b-%Y %H:%M") + ") > "
		#-jmanswer = input(inputString)
		#-jmif answer != "" :
		#-jm	self.endTime = datetime.strptime(answer, "%d-%b-%Y %H:%M")

	# setLocation
	#
	#		sets the location for which the data should be retrieved	

	#-jm def setLocation(self,location) :

		#-jm if location.upper() == "GILZE-RIJEN" :
		#-jm	self.locationCode = "06350"
		#-jm	self.locationName = location

	# readData
	#
	#		reads tthe data from the KNMI sites
	#			- first read a list of CSV files that should be processed
	#			- process each file
	#		at the end the wbgtTable is filled

	#-jm def readData(self) :

		#-jm files = self.api.list_files(self.startTime, self.endTime)
		#-jm  nrItems = len(files);
		#-jm print("%d files received ..." % nrItems)

		#-jm modFactor = 1
		#-jm if nrItems > 10 :
		#-jm 	modFactor = 10
		#-jm if nrItems > 100 :
		#-jm 	modFactor = 50

		#-jm self.wbgtTable = []
		#-jm for item,i in zip(files,range(1,nrItems+1)) :

			#-jm [time,wbgt,heatIndx] = self.api.getWBGTdata(item["filename"],self.locationCode)
			#-jm self.wbgtTable.append({"time" : time, "wbgt" : wbgt, "heatIndex" : heatIndx})

			# show process (not for all files)
	
			#-jm if ((i % modFactor) == 0) or (i==nrItems) :
			#0jm 	print("%d (of %d) files processed ..." % (i,nrItems))

		#-jm self.wbgtTable = sorted(self.wbgtTable, key=lambda x: x["time"])
		
	# list
	#
	#		lists the data in the wbgtTable		

	#-jm def list(self) :

		#-jm print(f"{'Time':<20} {'WBGT':>8} {'HeatIndex':>10}")
		#-jm print("-" * 40)

		#-jm for row in self.wbgtTable :
		#-jm 	print(
		#-jm		f"{row['time'].strftime('%d-%m-%Y %H:%M'):<20} "
		#-jm		f"{row['wbgt']:>8.1f} "
		#-jm 		f"{row['heatIndex']:>5.0f}"
		#-jm	)
	
	# plot
	#
	#		plots the data in the wbgtTable

	#-jm def plot (self,pltAreas = True) :
		
		# get the x and y data 
		#-jm time = [row["time"] for row in self.wbgtTable]
		#-jm wbgt = [row["wbgt"] for row in self.wbgtTable]

		#-jm fig, ax = plt.subplots()
		#-jm fig.set_facecolor("white")

		#-jm if len(time) < 50 :
		#=jm	ax.plot(time,wbgt,"*",markersize=6,color="blue")
		#-jm 	ax.plot(time,wbgt,linewidth=1,color="blue")
		#-jm else :
		#-jm 	ax.plot(time,wbgt,linewidth=1.5,color="blue")

		#-jm ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
		#-jm ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
		#-jm ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

		#-jm ax.set_ylim(16, 34)
		#-jm ax.set_xlabel("Time", fontweight="bold")
		#-jm ax.set_ylabel("WBGT (°C)", fontweight="bold")
		#-jm ax.set_title("WBGT at " + self.locationName + " (" + time[-1].strftime("%d-%b-%Y") +")",fontweight="bold")

		# box around plot

		#-jm for spine in ax.spines.values() :
			#-jm spine.set_visible(True)	

  	# if plotAreas is set shaded areas are plotted
	
		#-jm if pltAreas :

			# shaded areas

			#-jmax.axhspan(32.15, 34, facecolor="red", alpha=0.7)
			#-jm ax.axhspan(30.05, 32.15, facecolor="red", alpha=0.5)
			#-jm ax.axhspan(27.85, 30.05, facecolor="red", alpha=0.3)
			#-jm ax.axhspan(25.65, 27.85, facecolor=(0.95, 0.6, 0), alpha=0.45)
			#-jm ax.axhspan(22.25, 25.65, facecolor=(0.9, 0.9, 0), alpha=0.25)
			#-jm ax.axhspan(18.4, 22.25, facecolor=(0.9, 0.9, 0), alpha=0.15)

			# border lines
		
			#-jm ax.axhline(32.15, color='k', lw=0.5)	
			#-jm ax.axhline(30.03, color='k', lw=0.5)	
			#-jm ax.axhline(27.85, color='k', lw=0.5)	
			#-jm ax.axhline(25.65, color='k', lw=0.5)	
			#-jm ax.axhline(22.25, color='k', lw=0.5)	
			#-jm ax.axhline(18.4, color='k', lw=0.5)	
		
		# and show

		#-jm plt.show()


# OpenDataAPI
#
#			a class that acts as an interface with the KNMI open data platform
#
# modifications 
#		- 2024-06-10  JM   initial version

from datetime import datetime, timedelta, timezone
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from python.opendata import OpenDataAPI

class OpenWBGT : 

    # init
    #
    #		initialises the class
    #			- sets the default location
    #			- sets the API key
    #		  - set default start and stop dates
	
    def __init__ (self,location = "Gilze-Rijen") :
        
      print("in init")
	    
      # set the API key and the location

      self.apiKey = "eyJvcmciOiI1ZTU1NGUxOTI3NGE5NjAwMDEyYTNlYjEiLCJpZCI6IjBhZTg4MTI5MTAzOTQyN2FiMDVhNjM2NmNiOWQxMTE3IiwiaCI6Im11cm11cjEyOCJ9"
      self.setLocation(location)

      # use the OpenAPIdata class

      self.api = OpenDataAPI(dataset = "wet_bulb_globe_temperature", version = "3.0", token = self.apiKey)

      # sets the default start and stop date

      tz = timezone(timedelta(hours=2))
      self.startTime = datetime.now(tz) - timedelta(hours = 6)
      self.endTime = datetime.now(tz)

    # input
	  #
	  #   asks the user for start and stop dates

    def input(self) :
        
      inputString = "begin of WBGT data : (" + self.startTime.strftime("%d-%b-%Y %H:%M") + ") > "
      answer = input(inputString)
      if answer != "" :
        self.startTime = datetime.strptime(answer, "%d-%b-%Y %H:%M")

      inputString = "end of WBGT data : (" + self.endTime.strftime("%d-%b-%Y %H:%M") + ") > "
      answer = input(inputString)
      if answer != "" :
        self.endTime = datetime.strptime(answer, "%d-%b-%Y %H:%M")

    # setLocation
	  #
	  #		sets the location for which the data should be retrieved	

    def setLocation(self, location) :
            
      if location.upper() == "GILZE-RIJEN" :
        self.locationCode = "06350"
        self.locationName = location

    # readData
    #
    #		reads tthe data from the KNMI sites
    #			- first read a list of CSV files that should be processed
    #			- process each file
    #		at the end the wbgtTable is filled

    def readData(self) :
         
      files = self.api.list_files(self.startTime, self.endTime)
      nrItems = len(files);
      print("%d files received ..." % nrItems)

      modFactor = 1
      if nrItems > 10 :
        modFactor = 10
      if nrItems > 100 :
        modFactor = 50

      self.wbgtTable = []
      for item,i in zip(files,range(1,nrItems+1)) :

        [time,wbgt,heatIndx] = self.api.getWBGTdata(item["filename"],self.locationCode)
        self.wbgtTable.append({"time" : time, "wbgt" : wbgt, "heatIndex" : heatIndx})

			  # show process (not for all files)
	
        if ((i % modFactor) == 0) or (i==nrItems) :
          print("%d (of %d) files processed ..." % (i,nrItems))

      self.wbgtTable = sorted(self.wbgtTable, key=lambda x: x["time"])

    # plot
    #
    #		plots the data in the wbgtTable

    def plot(self, pltAreas = True) :

     	# get the x and y data 
		
      time = [row["time"] for row in self.wbgtTable]
      wbgt = [row["wbgt"] for row in self.wbgtTable]

      fig, ax = plt.subplots()
      fig.set_facecolor("white")

      if len(time) < 50 :
        ax.plot(time,wbgt,"*",markersize=6,color="blue")
        ax.plot(time,wbgt,linewidth=1,color="blue")
      else :
        ax.plot(time,wbgt,linewidth=1.5,color="blue")

      ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
      ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
      ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

      ax.set_ylim(16, 34)
      ax.set_xlabel("Time", fontweight="bold")
      ax.set_ylabel("WBGT (°C)", fontweight="bold")
      ax.set_title("WBGT at " + self.locationName + " (" + time[-1].strftime("%d-%b-%Y") +")",fontweight="bold")

		  # box around plot

      for spine in ax.spines.values() :
        spine.set_visible(True)	

  	  # if plotAreas is set shaded areas are plotted
	
      if pltAreas :

			# shaded areas

        ax.axhspan(32.15, 34, facecolor="red", alpha=0.7)
        ax.axhspan(30.05, 32.15, facecolor="red", alpha=0.5)
        ax.axhspan(27.85, 30.05, facecolor="red", alpha=0.3)
        ax.axhspan(25.65, 27.85, facecolor=(0.95, 0.6, 0), alpha=0.45)
        ax.axhspan(22.25, 25.65, facecolor=(0.9, 0.9, 0), alpha=0.25)
        ax.axhspan(18.4, 22.25, facecolor=(0.9, 0.9, 0), alpha=0.15)

        # border lines

        ax.axhline(32.15, color='k', lw=0.5)	
        ax.axhline(30.03, color='k', lw=0.5)	
        ax.axhline(27.85, color='k', lw=0.5)	
        ax.axhline(25.65, color='k', lw=0.5)	
        ax.axhline(22.25, color='k', lw=0.5)	
        ax.axhline(18.4, color='k', lw=0.5)	

		  # and show (make some space around it)

      print();
      plt.show()

  	# list
    #
    #		lists the data in the wbgtTable	

    def list(self) :
        
      print(f"{'Time':<20} {'WBGT':>8} {'HeatIndex':>10}")
      print("-" * 40)

      for row in self.wbgtTable :
        print(
          f"{row['time'].strftime('%d-%m-%Y %H:%M'):<20} "
          f"{row['wbgt']:>8.1f} "
          f"{row['heatIndex']:>5.0f}"
        )
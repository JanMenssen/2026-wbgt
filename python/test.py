# OpenDataAPI
#
#			a class that acts as an interface with the KNMI open data platform
#
# modifications 
#		- 2024-06-10  JM   initial version

from datetime import datetime,timedelta, timezone
import requests
import csv
import os

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

    def plot(self) :
        
      print("in plot")
  
  	# list
    #
    #		lists the data in the wbgtTable	

    def list(self) :
        
      print("in list")  
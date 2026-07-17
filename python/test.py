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
        
      print("in input") 

    # setLocation
	  #
	  #		sets the location for which the data should be retrieved	

    def setLocation(self) :
            
      print(" in seocation")    

    # readData
    #
    #		reads tthe data from the KNMI sites
    #			- first read a list of CSV files that should be processed
    #			- process each file
    #		at the end the wbgtTable is filled

    def readData(self) :
        
      print("in readData")  

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
# OpenDataAPI
#
#			a class that acts as an interface with the KNMI open data platform
#
# modifications 
#		- 2024-06-10  JM   initial version

from datetime import datetime,timedelta
import requests
import csv
import os

class OpenWBGT : 

	# init
	#
	#		initialises the class,
	
    def __init__ (self) :
        
        print("in init")

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
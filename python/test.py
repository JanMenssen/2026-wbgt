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
	
		def __init__(self, dataset, version, token) :

			self.base_url = "https://api.dataplatform.knmi.nl/open-data/v1/datasets/" + dataset +"/versions/" + version
			self.headers = {"Authorization": token}

		# list_files
		#
		#			returns a vector with files to process

		def list_files(self,start_time,end_time) :

			files = []

			# Create a string for the start and end time. Note there is a 2 hours offset
			# for the KNMI data (timezone ?)

			start_time = start_time - timedelta(hours=2)
			knmiStartFile  = "wbgt_" + start_time.strftime("%Y%m%d%H%M") + ".csv"
	
			end_time = end_time - timedelta(hours=2)
			knmiEndFile = "wbgt_"+ end_time.strftime("%Y%m%d%H%M") + ".csv"
			
			# now generate the URL and request all files, if there are more than 1000 

			tmpurl = self.base_url + "/files?maxKeys=1000&sorting=desc&orderBy=filename&begin=" + knmiStartFile + "&end=" + knmiEndFile
			response = requests.get(url = tmpurl,headers = self.headers)

			# only for valid response
		
			if response.status_code == 200 :
				
				files = response.json()["files"]
	
				# check more files available

				while "nextPageToken" in response.json() :

					token = response.json()["nextPageToken"]
					tmpURL = self.base_url + "/files?maxKeys=1000&sorting=desc&orderBy=filename&begin=" + knmiStartFile + "&end=" + knmiEndFile + "&nextPageToken=" + token

					response = requests.get(url = tmpURL, headers= self.headers)
					if response.status_code == 200 :
						files = files + response.json()["files"]

			return files
		
    	# input
	#
	#    asks the user for start and stop dates

	  def input(self) :
		
      print("in input")

		#-jm inputString = "begin of WBGT data : (" + self.startTime.strftime("%d-%b-%Y %H:%M") + ") > "
		#-jmanswer = input(inputString)
		#-jmif answer != "" :
		#-jm		self.startTime = datetime.strptime(answer, "%d-%b-%Y %H:%M")

		#-jminputString = "end of WBGT data : (" + self.endTime.strftime("%d-%b-%Y %H:%M") + ") > "
		#-jmanswer = input(inputString)
		#-jmif answer != "" :
		#-jm	self.endTime = datetime.strptime(answer, "%d-%b-%Y %H:%M")


		# getWBGTdata
		#
		#			returns the time, wbgtvalue and heatindex from the given file

		def getWBGTdata(self,filename,weatherStation) :
						
			time = None
			wbgt = None
			heatIndex = None

			# convert to time
			
			time = datetime.strptime(filename[5:17],"%Y%m%d%H%M") + timedelta(hours = 2)

			# download the file

			downloadURL = self.base_url + "/files/" + filename + "/url"     
			
			response  = requests.get(url = downloadURL, headers = self.headers)
			tmpURL = response.json()["temporaryDownloadUrl"]
			
			try :
				with requests.get(url = tmpURL, stream=True) as response :
					response.raise_for_status()
					with open(filename,"wb") as file :
						for chunk in response.iter_content(chunk_size = 8192) :
							file.write(chunk)
						file.close()
			except :
				print("unable to read" + filename +"...")
    
			# read the file, first line is skipped and find the desired station

			with open(filename, newline="", encoding="utf-8") as csvfile :
				
				next(csvfile)
				reader = csv.DictReader(csvfile)
				
				for row in reader:
					if row["station"] == weatherStation :
						wbgt = float(row["wbgt"])
						heatIndex = float(row["heat_force"])
			
			csvfile.close()

			# done, remove the file

			os.remove(filename)
			return time,wbgt,heatIndex


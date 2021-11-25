""""
Use Python 3
Workload Patch Script made by HatchiFR
"""

##Inputs
username = ""
# from https://github.com/user/settings/tokens
token = ""

##Folders
#Download Directory
DownloadDirectory = "tempDir"
#SD Directory
SDDirectory = "SD"
#Tools Directory
ToolsDirectory= "Tools"
#Folders
ScriptFolders = [DownloadDirectory, SDDirectory, ToolsDirectory]
SDFolders = ["atmosphere", "bootloader", "switch"]

##.:::. Module .:::.
#Requests is needed for web call
import requests
#Progress Bar that working with requests
from clint.textui import progress
#Json is needed to manage Json
import json
#OS.PATH & SHUTIL is needed to manage files
import os.path
import shutil
#Colorama is needed to have colorfoul print
from colorama import init, Fore, Back, Style
#Re is used for regex
import re
#ZipFile, used to unzip
import zipfile

##.:::. Class .:::.
class package:
	def __init__(self, packagename, repository, releasetype, filename, filesearch,url, version, filetype):
		self.packagename = packagename
		self.repository = repository
		self.releasetype = releasetype
		self.filename = filename
		self.filesearch = filesearch
		self.url = url
		self.version = version
		self.filetype = filetype

##.:::. Functions .:::.
def func_RelocateCurrentWorkingFolder():
	os.chdir(os.path.dirname(__file__))

def func_CleanSDFolder():
	os.rmdir(SDDirectory)
	print(Style.BRIGHT + Fore.MAGENTA + "LOG : " + folder + " folder deleted")

def func_SkeletonFolders():
	for folder in ScriptFolders:
		if not (os.path.exists(folder)):
			os.mkdir(folder)
			print(Style.BRIGHT + Fore.MAGENTA + "LOG : " + folder + " folder created")
	for folder in SDFolders:
		if not (os.path.exists(SDDirectory + "/" + folder)):
			os.mkdir(SDDirectory + "/" + folder)
			print(Style.BRIGHT + Fore.MAGENTA + "LOG : " + SDDirectory + "/" + folder + " folder created")

def func_ImportJson():
	with open('data.json') as f:
		data = json.load(f)
		f.close()
	return data

def func_UpdateJson(jsondata):
	with open('data.json', "w") as f:
		json.dump(jsondata, f, indent=4)
		f.close()

def func_CheckGithubRepository(data,gh_session):
	#Check last release version of needed repository
	#Scrap Repository informations and tranform data to exploitable Json
	if data.releasetype == "latest":
		githubresult = json.loads(gh_session.get("https://api.github.com/repos/" + data.repository + "/releases/latest").text)
	if data.releasetype == "pre-release":
		githubresult = (json.loads(gh_session.get("https://api.github.com/repos/" + data.repository + "/releases").text))[0]

	#Check if newer version exist
	if data.version >= githubresult["tag_name"]:
		print(Style.BRIGHT + Fore.YELLOW + "No update are available for " + Fore.WHITE + data.packagename + Fore.YELLOW + " version is : " + Fore.WHITE + data.version)
		#Return False, there is a no update
		return False
	else:
		searchresult = func_SearchFileGithubRepository(githubresult, data)
		#Add/Update package information
		data.filename = searchresult["name"]
		data.url = searchresult["browser_download_url"]
		data.version = githubresult["tag_name"]

		#Print if a new version is available
		print(Style.BRIGHT + Fore.CYAN + "New update is available ! Latest " + Fore.WHITE + data.packagename + Fore.CYAN + " version is : " + Fore.WHITE + data.version)
		#Return True, there is a new update
		return True

def func_SearchFileGithubRepository(githubresult, data):
	#Search in all assets if there is the good file, return it if it's founded
	for asset in githubresult["assets"]:
		if re.findall("%s" % data.filesearch, asset["name"], re.IGNORECASE):
			return asset

def func_DownloadFiles(data):
	print(Style.BRIGHT + Fore.GREEN + "Downloading Latest version of " + Fore.WHITE + data.packagename)
	# Make http request for remote file data
	r = requests.get(data.url, stream=True)
	path = DownloadDirectory + "/" + data.filename
	with open(path, 'wb') as f:
	    total_length = int(r.headers.get('content-length'))
	    for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
	        if chunk:
	            f.write(chunk)
	            f.flush()

def func_UnzipFiles(data,SDDirectory,DownloadDirectory):
	with zipfile.ZipFile(DownloadDirectory + "/" + data.filename ,"r") as zip_ref:
		zip_ref.extractall(SDDirectory)

##.:::. Main .:::.
#Change current working dir to script location folder
os.chdir(os.path.dirname(__file__))

#Futur Function to clean on demand the SD Folder
#func_CleanSDFolder()

#Check if SkeletonFolders exist if not create it
func_SkeletonFolders()

#Import JSON data file to a Dict
jsondata = func_ImportJson()

#Create a re-usable session object with the user creds in-built
gh_session = requests.Session()
gh_session.auth = (username, token)

#Counter to find the index to update data in dict
c = 0
#Let's iterate for each entry in the jsondata list (jsondata["soft"] is a list)
for i in jsondata["soft"]:
	#The double asterisks ** expands the dictionary jsondata to allow every key-value pair from dict to be passed to the __init__() method of Class.
	data = package(**i)
	#If there is an update (return True) we are doing other task else nothing to do for this package
	if func_CheckGithubRepository(data,gh_session):
		func_DownloadFiles(data)
		#Check if file is a ZipFile
		if re.findall("%s" % ".*.zip", data.filename, re.IGNORECASE):
			func_UnzipFiles(data,SDDirectory,DownloadDirectory)

		#Check if file is a bootfile to convert
		if data.filetype == "BootFile":
			filename = DownloadDirectory + "/" + data.filename
			exec(open(ToolsDirectory + "/tx_custom_boot.py").read())
			print(Style.BRIGHT + Fore.YELLOW + "LOG : bootfile.dat for " + data.packagename + " generated")

		#Check if file is a Payload
		if data.filetype == "Payload":
			shutil.copyfile(DownloadDirectory + "/" + data.filename, SDDirectory + "/bootloader/payloads/" + data.filename)

		#Check if file is a Homebrew
		if data.filetype == "Homebrew":
			shutil.copyfile(DownloadDirectory + "/" + data.filename, SDDirectory + "/switch/" + data.filename)

	#Convert data to dict format and update jsondata entry
	jsondata["soft"][c] = data.__dict__
	#Count the index of the jsondata[soft] dict
	c += 1

#Write new value in JSON file
func_UpdateJson(jsondata)
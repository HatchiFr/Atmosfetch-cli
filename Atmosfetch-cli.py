""""
Use Python 3
Workload Patch Script made by HatchiFR
Version 1.0
Date 27/11/2021
"""

##Inputs
username = ""
# from https://github.com/settings/tokens
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
SDFolders = ["atmosphere", "bootloader", "/bootloader/payloads/", "switch"]
#CleanMode
cleanmode = False

##.:::. Module .:::.
# Argparse to manage args
import argparse
#Requests is needed for web call
import requests
#Progress Bar that working with requests
from clint.textui import progress
#Json is needed to manage Json
import json
#OS.PATH & SHUTIL is needed to manage files
import os.path
import shutil
#Colorama is needed to have colourful print
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
	os.chdir(os.path.dirname(os.path.abspath(__file__)))

def func_CleanSDFolder():
	try:
		shutil.rmtree(SDDirectory, ignore_errors=True)
		print(Style.BRIGHT + Fore.MAGENTA + "LOG : Directory " + SDDirectory + " has been removed successfully")
	except OSError as error:
		print(error)

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
	#Scrap Repository informations and transform data to exploitable Json
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
# Initiate the parser
print(Style.BRIGHT + Fore.WHITE + "Welcome on AtmosFetch !")
print(Style.BRIGHT + Fore.WHITE + "Script created by HatchiFR")
print(Style.BRIGHT + Fore.WHITE + "Version 1.0 - 24/11/2021")

parser = argparse.ArgumentParser()
parser.add_argument("-he", "--hekate", help="Convert hekate.bin as boot.dat", action="store_true")
parser.add_argument("-at", "--atmosphere", help="Convert fusee.bin as boot.dat", action="store_true")
parser.add_argument("-c", "--clean", help="Remove SD folder and redownload all", action="store_true")

# Read arguments from the command line
args = parser.parse_args()

#Check if someone is using -he and -at same time ...
if (args.atmosphere and args.hekate):
	print(Style.BRIGHT + Fore.RED + "ERROR : You must specify only one bootloader file in args !")
	print(Style.BRIGHT + Fore.YELLOW + "LOG : Please check atmosfetch-cli.py -h")
	exit()

#Change current working dir to script location folder
os.chdir(os.path.dirname(os.path.abspath(__file__)))

if args.clean :
	#Function to clean on demand the SD Folder
	cleanmode = True
	print(Style.BRIGHT + Fore.GREEN + "   ________    _________    _   __")
	print(Style.BRIGHT + Fore.GREEN + "  / ____/ /   / ____/   |  / | / /")
	print(Style.BRIGHT + Fore.GREEN + " / /   / /   / __/ / /| | /  |/ / ")
	print(Style.BRIGHT + Fore.GREEN + "/ /___/ /___/ /___/ ___ |/ /|  /  ")
	print(Style.BRIGHT + Fore.GREEN + "\\____/_____/_____/_/_ |_/_/_|_/   ")
	print(Style.BRIGHT + Fore.GREEN + "   /  |/  / __ \\/ __ \\/ ____/     ")
	print(Style.BRIGHT + Fore.GREEN + "  / /|_/ / / / / / / / __/        ")
	print(Style.BRIGHT + Fore.GREEN + " / /  / / /_/ / /_/ / /___        ")
	print(Style.BRIGHT + Fore.GREEN + "/_/  /_/\\____/_____/_____/        ")
	func_CleanSDFolder()

#Check if SkeletonFolders exist if not create it
func_SkeletonFolders()

#Import JSON data file to a Dict
jsondata = func_ImportJson()

#Create a reusable session object with the user creds in-built
gh_session = requests.Session()
gh_session.auth = (username, token)

#Counter to find the index to update data in dict
index = 0
#Update found
NeedToUpdate = False
#Let's iterate for each entry in the jsondata list (jsondata["soft"] is a list)
for i in jsondata["soft"]:
	#The double asterisks ** expands the dictionary jsondata to allow every key-value pair from dict to be passed to the __init__() method of Class.
	data = package(**i)
	#If there is an update (return True) or if we are ine Clean Mode !
	if (func_CheckGithubRepository(data,gh_session) or cleanmode):

		#If there is an update, the value becomes True to start some actions.
		NeedToUpdate=True

		#Start download function with data object as argument
		func_DownloadFiles(data)

		#Check if file is a ZipFile and unzip it in SD folder
		if re.findall("%s" % ".*.zip", data.filename, re.IGNORECASE):
			func_UnzipFiles(data,SDDirectory,DownloadDirectory)

		#Check if file is a Payload
		if data.filetype == "Payload":
			shutil.copyfile(DownloadDirectory + "/" + data.filename, SDDirectory + "/bootloader/payloads/" + data.filename)

		#Check if file is a Homebrew
		if data.filetype == "Homebrew":
			shutil.copyfile(DownloadDirectory + "/" + data.filename, SDDirectory + "/switch/" + data.filename)

		#ATMOSPHERE FUSEE PART
		#Manage Atmosphere boot.data file case
		#Check if it's a bootloader payload to convert and check the package name
		if data.filetype == "Bootloader" and data.packagename == "Atmosphere-Fusee":
			#Copy fusee.bin in hekate payload folder
			shutil.copyfile(DownloadDirectory + "/" + data.filename, SDDirectory + "/bootloader/payloads/" + data.filename)
			#Check args : If -at or if -c or if -at and -c or no args but not -he
			if (args.atmosphere or (args.clean and not args.hekate) or (not (any(vars(args).values())))):
				filename = DownloadDirectory + "/" + data.filename
				#Convert bootloader payload as boot.dat
				exec(open(ToolsDirectory + "/tx_custom_boot.py").read())
				print(Style.BRIGHT + Fore.YELLOW + "LOG : bootfile.dat for " + data.packagename + " generated")
				#Copy fusee.bin on SD root as payload.bin for RCM Injector
				shutil.copyfile(filename, SDDirectory + "/payload.bin")
				
		#HEKATE PART
		#Check if it's a bootloader payload to convert and check the package name
		if data.filetype == "Bootloader" and data.packagename == "Hekate":
			#Search Hekate file in SD folder
			for file in os.listdir(SDDirectory):
				if (file.startswith("hekate")):
					filename = SDDirectory + "/" + file
			#Copy hekate bootloader payload in atmosphere folder as reboot_payload.bin file to reboot on it
			shutil.copyfile(filename, SDDirectory + "/atmosphere/" + "reboot_payload.bin")
			#Manage Hekate boot.data file case
			if (args.hekate): 
				#Convert hekate_ctcaer_X.X.X.bin file as boot.dat
				exec(open(ToolsDirectory + "/tx_custom_boot.py").read())
				print(Style.BRIGHT + Fore.YELLOW + "LOG : bootfile.dat for " + data.packagename + " generated")
				#Rename hekate_ctcaer_X.X.X.bin file as payload.bin
				shutil.move(filename, SDDirectory + "/payload.bin")
			#Remove hekate_ctcaer_X.X.X.bin file if it's atmosphere fusee mode
			if (args.atmosphere or (args.clean and not args.hekate) or (not (any(vars(args).values())))):
				os.remove(filename)
				
	#Convert data to dict format and update jsondata entry
	jsondata["soft"][index] = data.__dict__
	#Count the index of the jsondata[soft] dict
	index += 1

	#Check package name to get version for zipfilename
	if data.packagename == "Atmosphere":
		AtmosphereVersion = data.version
	if data.packagename == "Hekate":
		HekateVersion = data.version.replace("v", "")
	if data.packagename == "Patches":
		PatchesVersion = data.version

#If there is any modification : Write new information in jsonfile and create a new zip file.
if (NeedToUpdate):
	#Write new value in JSON file
	func_UpdateJson(jsondata)
	#Creating ZIP
	zipname = "Pack.Atmosphere." + AtmosphereVersion + ".Hekate." + HekateVersion + ".Sigpatch.FW." + PatchesVersion.split("-")[0] + ".AtmoVersion." + PatchesVersion.split("-")[1]
	shutil.make_archive(zipname, 'zip', SDDirectory)
# 🌌 Atmosfetch (CLI)
 
<img src="https://i.imgur.com/WZY0BlW.jpg">
AtmosFetch is a python script to download latest Atmosphere release with some extra homebrews and prepare all needed SD files.

## 📓 Informations

- Atmosfetch have a version management : It download only needed updates in normal mode.
- You can simply add/edit/remove packages in the data.json file.
- Atmosfetch can convert bootloader file into boot.dat for SXOS RCM injector users.
- Atmosphere CFW will reboot every time on Hekate (reboot_payload.bin).

## 🔧 Prerequisites

- Python 3: https://www.python.org/downloads/
- Only tested on Python 3.10
- Python 3 must be well configured in your environnement PATH.
- You must install some python packages : pip install requests clint colorama

## 🌠 User's guide

There is 3 available modes with Atmosfetch :

-at : Atmosphere as default boot SXOS RCM (boot.dat).  
-he : Hekate as default boot SXOS RCM (boot.dat).
-c  : Clean mode, delete SD folder and redownload all even if there isn't updates.

Exemple of usage : python Atmosfetch-cli.py -at

By default, if there is no arguments Atmosphere fusee.bin will be used as payload.bin and boot.dat.
You can combine a boot mode with clean mode. 

When the script finish to execute : there is a SD folder with files that you can copy on your SD as is and a end zip file that you can share or keep for archives.

## ☝️ FAQ

Q : Did Atmosfetch will download everything everytime ?
A : No, Atmosfetch have a version management process, it will download only the package that have an update.

Q : How to clean and redownload eveything?
A : Use clean mode with -c as argument.


## 🚀 Thanks to the developer for their work

- SciresM (Atmosphère & DayBreak) : https://github.com/Atmosphere-NX/Atmosphere
- SciresM & FlagBrew (Checkpoint) : https://github.com/FlagBrew/Checkpoint
- CTCaer (Hekate) : https://github.com/CTCaer/hekate
- CTCaer & Hexkiz (TX Custom Boot) : https://gist.github.com/CTCaer/13c02c05daec9e674ba00ce5ac35f5be
- WerWolv (Edizon) : https://github.com/WerWolv/EdiZon
- Mtheall (ftpd) : https://github.com/mtheall/ftpd
- J-D-K (JKSV) : https://github.com/J-D-K/JKSV
- Adubbz (Tinfoil) : https://github.com/Adubbz/Tinfoil (Closed Source)
- Mrdude2478 (TinWoo) : https://github.com/mrdude2478/TinWoo/
- Meganukebmp (Switch_90DNS_tester) : https://github.com/meganukebmp/Switch_90DNS_tester
- Sigpatch : https://github.com/ITotalJustice/patches

Also thanks to SigHya community for the original idea : https://github.com/Lunyyx/AtmosphereVanillaFetcher-cli

Special thanks to SciresM and all the Reswitched team who made this possible !

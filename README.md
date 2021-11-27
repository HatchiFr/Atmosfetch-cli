# 🌌 Atmosfetch (CLI)
 
<img src="https://i.imgur.com/WZY0BlW.jpg">
AtmosFetch is a python script to download latest Atmosphere release with some extra homebrews and prepare all needed SD files.


## 🔧 Prerequisites

- Python 3: https://www.python.org/downloads/
- Only tested on Python 3.10
- Python 3 must be well configured in your environnement PATH.
- You must install some python packages : pip install requests clint colorama

## 🌠 User's guide

There is 3 possibles modes with Atmosfetch :
-at : Atmosphere as default boot SXOS RCM (boot.dat)  
-he : Hekate as default boot SXOS RCM (boot.dat)
-c : clean mode, delete SD folder and redownload all even if there is'nt updates

Exemple : python Atmosfetch-cli.py -at

By default, if there is no arguments Atmosphere will be used as default boot.

You can combine a boot mode with clean mode.  

When the script finish to execute : there is a SD folder with files that you can copy on your SD as is and a end zip file that you can share or keep for archives.


Thanks to the developer for their work

- SciresM (Atmosphère & DayBreak) : https://github.com/Atmosphere-NX/Atmosphere
- SciresM & FlagBrew (Checkpoint) : https://github.com/FlagBrew/Checkpoint
- CTCaer (Hekate) : https://github.com/CTCaer/hekate
- CTCaer & Hexkiz (TX Custom Boot) : https://gist.github.com/CTCaer/13c02c05daec9e674ba00ce5ac35f5be
- WerWolv (Edizon) : https://github.com/WerWolv/EdiZon
- Mtheall (ftpd) : https://github.com/mtheall/ftpd
- J-D-K (JKSV) : https://github.com/J-D-K/JKSV
- Liuervehc (nxmtp) : https://github.com/liuervehc/nxmtp/
- Joel16 (NX-Shell) : https://github.com/joel16/NX-Shell
- Adubbz (Tinfoil) : https://github.com/Adubbz/Tinfoil (Closed Source)
- Mrdude2478 (TinWoo) : https://github.com/mrdude2478/TinWoo/
- XorTroll (Goldleaf) : https://github.com/XorTroll/Goldleaf
- Meganukebmp (Switch_90DNS_tester) : https://github.com/meganukebmp/Switch_90DNS_tester
- PoloNX (sigpatch-downloader) : https://github.com/PoloNX/sigpatch-downloader
- Sigpatch : https://github.com/THZoria/patches

Special thanks to SciresM and all the Reswitched team who made this possible !

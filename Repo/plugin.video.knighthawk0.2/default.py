import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,base64,sys,xbmcvfs
import shutil
import urllib2,urllib
import re
import extract
import downloader
import time
import plugintools
from addon.common.addon import Addon
from addon.common.net import Net
import CheckPath
import zipfile
import ntpath


addon_id = 'plugin.video.knighthawk'
ADDON = xbmcaddon.Addon(id=addon_id)
AddonID='plugin.video.knighthawk'
AddonTitle="[COLOR lime]Knight Hawk[/COLOR] [COLOR white]Wizard[/COLOR]"
dialog       =  xbmcgui.Dialog()
net = Net()
HOME         =  xbmc.translatePath('special://home/')
dp           =  xbmcgui.DialogProgress()
U = ADDON.getSetting('User')
FANART = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
ICON = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
ART = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art/'))
VERSION = "1.19"
DBPATH = xbmc.translatePath('special://database')
TNPATH = xbmc.translatePath('special://thumbnails');
PATH = "knighthawk Wizard"            
BASEURL = "http://schismtv.pcriot.com/repo"
H = 'http://'
skin         =  xbmc.getSkinDir()
EXCLUDES     = ['backupdir','plugin.video.knighthawk0.2','script.module.addon.common','repository.knighthawk.addons','backup','backup.zip']

ARTPATH      =  '' + os.sep
UPDATEPATH     =  xbmc.translatePath(os.path.join('special://home/addons',''))
UPDATEADPATH	=  xbmc.translatePath(os.path.join('special://home/userdata/addon_data',''))
USERDATA     =  xbmc.translatePath(os.path.join('special://home/userdata',''))
MEDIA        =  xbmc.translatePath(os.path.join('special://home/media',''))
AUTOEXEC     =  xbmc.translatePath(os.path.join(USERDATA,'autoexec.py'))
AUTOEXECBAK  =  xbmc.translatePath(os.path.join(USERDATA,'autoexec_bak.py'))
ADDON_DATA   =  xbmc.translatePath(os.path.join(USERDATA,'addon_data'))
PLAYLISTS    =  xbmc.translatePath(os.path.join(USERDATA,'playlists'))
DATABASE     =  xbmc.translatePath(os.path.join(USERDATA,'Database'))
ADDONS       =  xbmc.translatePath(os.path.join('special://home','addons',''))
CBADDONPATH  =  xbmc.translatePath(os.path.join(ADDONS,AddonID,'default.py'))
GUISETTINGS  =  os.path.join(USERDATA,'guisettings.xml')
GUI          =  xbmc.translatePath(os.path.join(USERDATA,'guisettings.xml'))
GUIFIX       =  xbmc.translatePath(os.path.join(USERDATA,'guifix.xml'))
INSTALL      =  xbmc.translatePath(os.path.join(USERDATA,'install.xml'))
FAVS         =  xbmc.translatePath(os.path.join(USERDATA,'favourites.xml'))
SOURCE       =  xbmc.translatePath(os.path.join(USERDATA,'sources.xml'))
ADVANCED     =  xbmc.translatePath(os.path.join(USERDATA,'advancedsettings.xml'))
PROFILES     =  xbmc.translatePath(os.path.join(USERDATA,'profiles.xml'))
RSS          =  xbmc.translatePath(os.path.join(USERDATA,'RssFeeds.xml'))
KEYMAPS      =  xbmc.translatePath(os.path.join(USERDATA,'keymaps','keyboard.xml'))

notifyart    =  xbmc.translatePath(os.path.join(ADDONS,AddonID,'resources/'))
skin         =  xbmc.getSkinDir()
userdatafolder = xbmc.translatePath(os.path.join(ADDON_DATA,AddonID))
UPDATELIST     = ['plugin.video.mutttsnutz','plugin.video.Jeckyll-Hyde']
zip = 'special://home/addons/plugin.video.knighthawk'
urlbase      =  'None'
mastercopy   =  ADDON.getSetting('mastercopy')
dialog = xbmcgui.Dialog()
urlupdate =  ""
updatename =  "schismtv_update"
backupdir    =  xbmc.translatePath(os.path.join('special://home/backupdir',''))
USB          =  xbmc.translatePath(os.path.join('special://home/addons/plugin.video.knighthawk',''))
mybackuppath =  xbmc.translatePath(os.path.join('special://home',''))
EXCLUDESDATA    = ['backupdir','favourites.xml', 'sources.xml' , 'Thumbnails', 'guisettings.xml','script.skinshortcuts','script.module.addon.common','repository.knighthawk.addons','backup','backup.zip']
INCLUDEGUI = ['guisettings.xml', 'favourites.xml']
SKINSHORTCUTS = ['script.skinshortcuts']
class Gui(xbmcgui.WindowXMLDialog):
    def __init__(self, *args, **kwargs):
        xbmcgui.WindowXMLDialog.__init__(self)
        self.header = kwargs.get("header")
        self.content = kwargs.get("content")

    def onInit(self):
        self.getControl(1).setLabel(self.header)
        self.getControl(5).setText(self.content)

path   = xbmcaddon.Addon().getAddonInfo('path').decode("utf-8")

logfile = xbmcvfs.File(os.path.join(path, 'changelog.txt'))
text = logfile.read()
logfile.close()



def BACKUP():  

    to_backup = xbmc.translatePath(os.path.join('special://','home/userdata/addon_data'))
    backup_zip = xbmc.translatePath(os.path.join(backupdir,'addon_data.zip'))
    backup_path = xbmc.translatePath(os.path.join(backupdir,'backup'))    
    
    dp = xbmcgui.DialogProgress()
    dp.create("BACKUP/RESTORE","Backing Up",'', 'Please Wait')

    choice = xbmcgui.Dialog().yesno("EXPERIMENTAL BACKUP RESTORE TOOL", 'Info: Before performing a backup you should clear your thumbnails as it may results in large file size...', 'This is EXPERIMENTAL!', 'In addition you can install the USB/SDCARD BACKUP TOOL from the addons list to backup on different locations', yeslabel='Just Continue',nolabel='I will do it now... Exit')
    if choice == 0:
	 return
    elif choice == 1:
      dialog.ok("BACKUP/RESTORE", "Click OK to Start your backup", '','')
      exclude_dirs_full =  ['backupdir','plugin.video.knighthawk','repository.knighthawk.addons','script.skinshortcuts','plugin.program.super.favourites']
      exclude_files_full = ["xbmc.log","xbmc.old.log","kodi.log","kodi.old.log",'.DS_Store','.setup_complete','XBMCHelper.conf']
      message_header = "Backing up Addons Data"
      message1 = "Archiving..."
      message2 = ""
      message3 = "Please Wait"
      ARCHIVE_CB(to_backup, backup_zip, message_header, message1, message2, message3, exclude_dirs_full, exclude_files_full)
    
    

def ARCHIVE_CB(sourcefile, destfile, message_header, message1, message2, message3, exclude_dirs, exclude_files):
    zipobj = zipfile.ZipFile(destfile , 'w', zipfile.ZIP_DEFLATED)
    rootlen = len(sourcefile)
    for_progress = []
    ITEM =[]
    dp.create(message_header, message1, message2, message3)
    for base, dirs, files in os.walk(sourcefile):
        for file in files:
            ITEM.append(file)
    N_ITEM =len(ITEM)
    for base, dirs, files in os.walk(sourcefile):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        files[:] = [f for f in files if f not in exclude_files]
        for file in files:
            for_progress.append(file) 
            progress = len(for_progress) / float(N_ITEM) * 100  
            dp.update(int(progress),"Backing Up",'[COLOR yellow]%s[/COLOR]'%file, 'Please Wait')
            fn = os.path.join(base, file)
            zipobj.write(fn, fn[rootlen:])  
    zipobj.close()
    dp.close()
	
def BACKUPSKINSHORTCUTS():  
   choice = xbmcgui.Dialog().yesno("Skin Shortcuts", 'Do you want to Backup your Skin Shortcuts?', '', '', yeslabel='Yes',nolabel='No')
   if choice == 0:
	 return
   elif choice == 1:   
    to_backup = xbmc.translatePath(os.path.join('special://','home/userdata/addon_data'))
    backup_zip = xbmc.translatePath(os.path.join(backupdir,'backup_skinshortcuts.zip'))
    backup_path = xbmc.translatePath(os.path.join(backupdir,'backup'))    
    import zipfile
    dp = xbmcgui.DialogProgress()
    dp.create("BACKUP/RESTORE","Backing Up Skin Shortcuts",'', 'Please Wait')
    zipobj = zipfile.ZipFile(backup_zip , 'w', zipfile.ZIP_DEFLATED)
    rootlen = len(to_backup)
    for_progress = []
    ITEM =[]
    for base, dirs, files in os.walk(to_backup):
	dirs[:] = [d for d in dirs if d not in SKINSHORTCUTS]
	files[:] = [f for f in dirs if f not in SKINSHORTCUTS]
        for name in dirs:
            ITEM.append(name)
        for name in files:
            ITEM.append(name)
    N_ITEM =len(ITEM)
    for base, dirs, files in os.walk(to_backup):
	dirs[:] = [d for d in dirs if d in SKINSHORTCUTS]
        for name in files:
            for_progress.append(name) 
            progress = len(for_progress) / float(N_ITEM) * 100  
            dp.update(int(progress),"Backing Up",'[COLOR yellow]%s[/COLOR]'%name, 'Please Wait')
            fn = os.path.join(base, name)
            if not 'temp' in dirs:
                if not 'plugin.video.usbwizard' in dirs:
                   import time
                   CUNT= '01/01/1980'
                   FILE_DATE=time.strftime('%d/%m/%Y', time.gmtime(os.path.getmtime(fn)))
                   if FILE_DATE > CUNT:
                       zipobj.write(fn, fn[rootlen:])  
    zipobj.close()
    dp.close()
    dialog.ok("BACKUP/RESTORE", "SKIN Shortcuts Are Now Backed Up", '','')
    
	
def BACKUPGUI():  
    if os.path.exists(os.path.join(USERDATA,'guisettings.xml')):
       to_backup = xbmc.translatePath(os.path.join('special://','home/userdata'))	
       rootlen = len(to_backup)
       backup_ui_zip = xbmc.translatePath(os.path.join(backupdir,'backup_ui.zip'))
       zipobj = zipfile.ZipFile(backup_ui_zip , 'w', zipfile.ZIP_DEFLATED)
       fn = os.path.join(USERDATA, 'guisettings.xml')
       choice = xbmcgui.Dialog().yesno("Skin Settings", 'Do you want to backup your Skin settings?', '', '', yeslabel='Yes',nolabel='No')
       if choice == 0:
        return
       elif choice == 1:
	   dp.create("BACKUP/RESTORE","Backing Up Gui Settings",'', 'Please Wait')
	   zipobj.write(fn, fn[rootlen:])
	   dp.close()
	   dialog.ok("BACKUP/RESTORE", "Gui settings Are Now Backed Up", '','')
       

def BACKUPFAV():  
    if os.path.exists(os.path.join(USERDATA,'favourites.xml')):
       to_backup = xbmc.translatePath(os.path.join('special://','home/userdata'))	
       rootlen = len(to_backup)
       backup_ui_zip = xbmc.translatePath(os.path.join(backupdir,'backup_fav.zip'))
       zipobj = zipfile.ZipFile(backup_ui_zip , 'w', zipfile.ZIP_DEFLATED)
       fn = os.path.join(USERDATA, 'favourites.xml')
       choice = xbmcgui.Dialog().yesno("Gui Settings", 'Do you want to backup your favourites?', '', '', yeslabel='Yes',nolabel='No')
       if choice == 0:
            return
       elif choice == 1:
	   dp.create("BACKUP/RESTORE","Backing Up Favourites",'', 'Please Wait')
	   zipobj.write(fn, fn[rootlen:])
	   dp.close()
	   dialog.ok("BACKUP/RESTORE", "Favourites Are Now Backed Up", '','')          
    	   

def BACKUPSOURCE():  
    if os.path.exists(os.path.join(USERDATA,'sources.xml')):
       to_backup = xbmc.translatePath(os.path.join('special://','home/userdata'))	
       rootlen = len(to_backup)
       backup_ui_zip = xbmc.translatePath(os.path.join(backupdir,'backup_sources.zip'))
       zipobj = zipfile.ZipFile(backup_ui_zip , 'w', zipfile.ZIP_DEFLATED)
       fn = os.path.join(USERDATA, 'sources.xml')
       choice = xbmcgui.Dialog().yesno("Gui Settings", 'Do you want to backup your sources?', '', '', yeslabel='Yes',nolabel='No')
       if choice == 0:
            return
       elif choice == 1:
	   dp.create("BACKUP/RESTORE","Backing Up Sources",'', 'Please Wait')

	   zipobj.write(fn, fn[rootlen:])
	   dp.close()
	   dialog.ok("BACKUP/RESTORE", "Sources Are Now Backed Up", '','')	   
    INDEX()	   		   
	   
	
def READ_ZIP(url):

    import zipfile
    
    z = zipfile.ZipFile(url, "r")
    for filename in z.namelist():
        if 'guisettings.xml' in filename:
            a = z.read(filename)
            r='<setting type="(.+?)" name="%s.(.+?)">(.+?)</setting>'% skin
            
            match=re.compile(r).findall(a)
            print match
            for type,string,setting in match:
                setting=setting.replace('&quot;','') .replace('&amp;','&') 
                xbmc.executebuiltin("Skin.Set%s(%s,%s)"%(type.title(),string,setting))  
                
        if 'favourites.xml' in filename:
            a = z.read(filename)
            f = open(FAVS, mode='w')
            f.write(a)
            f.close()  
			               
        if 'sources.xml' in filename:
            a = z.read(filename)
            f = open(SOURCE, mode='w')
            f.write(a)
            f.close()    
                         
        if 'advancedsettings.xml' in filename:
            a = z.read(filename)
            f = open(ADVANCED, mode='w')
            f.write(a)
            f.close()                 

        if 'RssFeeds.xml' in filename:
            a = z.read(filename)
            f = open(RSS, mode='w')
            f.write(a)
            f.close()                 
            
        if 'keyboard.xml' in filename:
            a = z.read(filename)
            f = open(KEYMAPS, mode='w')
            f.write(a)
            f.close()                 
              
def RESTORE():
  	RESTOREADDONSETTINGS()
	RESTOREFAV()
	RESTORESOURCES()
	RESTORESKINSHORTCUTS()
	RESTOREGUI()
	killxbmc()

def BACKUPMENU():
  	BACKUP()
	BACKUPFAV()
	BACKUPSOURCE()
	BACKUPSKINSHORTCUTS()
	BACKUPGUI()
	
	
def XfinityInstaller():
    path = os.path.join(xbmc.translatePath('special://home'),'userdata', 'sources.xml')
    if not os.path.exists(path):
        f = open(path, mode='w')
        f.write('<sources><files><source><name>.[COLOR blue]X[/COLOR]finity Installer</name><path pathversion="1">http://xfinity.xunitytalk.com</path></source></files></sources>')
        f.close()
        return
        
    f   = open(path, mode='r')
    str = f.read()
    f.close()
    if not'http://xfinity.xunitytalk.com' in str:
        if '</files>' in str:
            str = str.replace('</files>','<source><name>.[COLOR blue]X[/COLOR]finity Installer</name><path pathversion="1">http://xfinity.xunitytalk.com</path></source></files>')
            f = open(path, mode='w')
            f.write(str)
            f.close()
        else:
            str = str.replace('</sources>','<files><source><name>.[COLOR blue]X[/COLOR]finity Installer</name><path pathversion="1">http://xfinity.xunitytalk.com</path></source></files></sources>')
            f = open(path, mode='w')
            f.write(str)
            f.close()

    	
def RESTOREADDONSETTINGS():
 if os.path.exists(os.path.join(backupdir,'addon_data.zip')):   
	import time
	
        
        dialog = xbmcgui.Dialog()
        choice = xbmcgui.Dialog().yesno("Addons Settings", 'Do you want to restore your addon settings?', '', '', yeslabel='Yes',nolabel='No')
        if choice == 0:
            return
        elif choice == 1:
			lib=xbmc.translatePath(os.path.join(backupdir,'addon_data.zip'))
			dp.create("[COLOR=blue][B]knigh thawk[/B][/COLOR] Custom Builds Tool","Restoring",'', 'Please Wait')
			dp.update(0,"", "Extracting Zip Please Wait")
			extract.all(lib,ADDON_DATA,dp)
			time.sleep(1)

	
def RESTOREGUI():
 if os.path.exists(os.path.join(backupdir,'backup_ui.zip')):   
        import time
        dialog = xbmcgui.Dialog()
        choice = xbmcgui.Dialog().yesno("GUI Settings", 'Do you want to restore your gui settings?', '', '', yeslabel='Yes',nolabel='No')
        if choice == 0:
          return
        elif choice == 1:
			
			
			
			lib=xbmc.translatePath(os.path.join(backupdir,'backup_ui.zip'))
			addonfolder = xbmc.translatePath(os.path.join('special://','home/userdata'))
			time.sleep(2)
			dp.create("[COLOR=blue][B]knighthawk[/B][/COLOR] Custom Builds Tool","Restoring",'', 'Please Wait')
			print '======================================='
			print addonfolder
			print '======================================='
			extract.all(lib,addonfolder,dp)
			dp.close()
			dialog.ok("BACKUP/RESTORE", "GUI settings Are Now restored", '','')	


 
def RESTOREFAV():
 if os.path.exists(os.path.join(backupdir,'backup_fav.zip')):
        import time
        dialog = xbmcgui.Dialog()
        choice = xbmcgui.Dialog().yesno("Favourites Settings", 'Do you want to restore your Favourites?', '', '', yeslabel='Yes',nolabel='No')
        if choice == 0:
            return
			
        elif choice == 1:
			
			

			lib=xbmc.translatePath(os.path.join(backupdir,'backup_fav.zip'))
			addonfolder = xbmc.translatePath(os.path.join('special://','home/userdata'))
			time.sleep(2)
			dp.create("[COLOR=blue][B]knighthawk[/B][/COLOR] Custom Builds Tool","Restoring",'', 'Please Wait')
			print '======================================='
			print addonfolder
			print '======================================='
			extract.all(lib,addonfolder,dp)
			dp.close()
			dialog.ok("BACKUP/RESTORE", "Favourites Are Now restored", '','')	
 
def RESTORESOURCES():
 if os.path.exists(os.path.join(backupdir,'backup_sources.zip')):
        import time
        dialog = xbmcgui.Dialog()
        choice = xbmcgui.Dialog().yesno("SOURCES Settings", 'Do you want to restore your Sources?', '', '', yeslabel='Yes',nolabel='No')
        if choice == 0:
            return
        elif choice == 1:
			
			

			lib=xbmc.translatePath(os.path.join(backupdir,'backup_sources.zip'))
			addonfolder = xbmc.translatePath(os.path.join('special://','home/userdata'))
			time.sleep(2)
			dp.create("[COLOR=blue][B]knighthawk[/B][/COLOR] Custom Builds Tool","Restoring",'', 'Please Wait')
			print '======================================='
			print addonfolder
			print '======================================='
			extract.all(lib,addonfolder,dp)
			dialog = xbmcgui.Dialog()
			dp.close()
			dialog.ok("BACKUP/RESTORE", "Sources Are Now restored", '','')	
 

			
def RESTORESKINSHORTCUTS():
 if os.path.exists(os.path.join(backupdir,'backup_skinshortcuts.zip')):
        import time
        dialog = xbmcgui.Dialog()
        choice = xbmcgui.Dialog().yesno("SKIN Settings", 'Do you want to restore your Skin Shortcuts', '', '', yeslabel='Yes',nolabel='No')
        if choice == 0:
            return
        elif choice == 1:
			
			

			lib=xbmc.translatePath(os.path.join(backupdir,'backup_skinshortcuts.zip'))
			addonfolder = xbmc.translatePath(os.path.join('special://','home/userdata/addon_data'))
			time.sleep(2)
			dp.create("[COLOR=blue][B]knighthawk[/B][/COLOR] Custom Builds Tool","Restoring",'', 'Please Wait')
			print '======================================='
			print addonfolder
			print '======================================='
			extract.all(lib,addonfolder,dp)
			dialog = xbmcgui.Dialog()
			dp.close()
			dialog.ok("BACKUP/RESTORE", "Skin Shortcuts Are Now restored", '','')	
 
			
def REFRESHALL():
    # dialog = xbmcgui.Dialog()
    # dialog.ok("BACKUP/RESTORE", "FORCE CLOSE/RESTART YOUR KODI", "","")
  killxbmc()
 
	
#Root menu of addon
def INDEX():
	if not os.path.exists(backupdir):
		os.makedirs(backupdir)
	addDir('[COLOR red][B]FRESH START[/B][/COLOR]','url',6,ART+'freshstart.png',FANART,'')
	addDir('[COLOR lime][B]Knight Hawk Builds [/B][/COLOR]',BASEURL,20,ART+'knighthawk.png',FANART,'')
	addDir('[COLOR yellow][B]UPDATE[/B][/COLOR]','url',1,ART+'update.png',FANART,'')
	addDir('[COLOR orange][B]Backup Settings[/B][/COLOR]','url',3,ART+'tool.png',FANART,'')
	addDir('[COLOR orange][B]Restore Settings[/B][/COLOR]','url',4,ART+'tool.png',FANART,'')
	#addDir('[COLOR gold][B]Unlock Build[/B][/COLOR]','url',11,ART+'tool.png',FANART,'')

def UPDATEMENU():
    linkupdate = OPEN_URL('https://archive.org/download/release_wizard/update_wizard.txt').replace('\n','').replace('\r','')
    matchupdate = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(linkupdate)
    
    if not matchupdate:
	dialog = xbmcgui.Dialog()
        dialog.ok('[COLOR=lime][B]Knight Hawk [/B][/COLOR][COLOR=white] Wizard[/COLOR]','NO Updates Currently Available','check back later.','')
	return
    dialog = Gui("DialogTextViewer.xml", path, header=xbmc.getLocalizedString(24036), content=text)
    dialog.doModal()	
    addDir('[COLOR red][B]FIRST Clean Addons Here[/B][/COLOR]','url',2,ART+'update.png',FANART,'')
    link = OPEN_URL('https://archive.org/download/release_wizard/update_wizard.txt').replace('\n','').replace('\r','')
    match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
    for name,url,iconimage,fanart,description in match:
        addDir(name,url,90,iconimage,fanart,description)
    setView('movies', 'MAIN')	
	
def BUILDMENU():
    
    link = OPEN_URL('https://archive.org/download/release_wizard/release_wizard.txt').replace('\n','').replace('\r','')
    match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
    for name,url,iconimage,fanart,description in match:
        addDir(name,url,90,iconimage,fanart,description)
    setView('movies', 'MAIN')

def UPDATER():
    linkupdate = OPEN_URL('https://archive.org/download/release_wizard/update_wizard.txt').replace('\n','').replace('\r','')
    matchupdate = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(linkupdate)
    
    if not matchupdate:
	dialog = xbmcgui.Dialog()
        dialog.ok('[COLOR=lime][B]knighthawk[/B][/COLOR][COLOR=white] Wizard[/COLOR]','NO Updates Currently Available','check back later.','')
	return           
    else:
        choice = xbmcgui.Dialog().yesno("UPDATE FOUND", 'Do you want to update your Build?', '', 'Obsolete Addons will be removed!', yeslabel='Yes',nolabel='No')
        if choice == 0:
            return
        elif choice == 1:
            dp.create("[COLOR=lime][B]Knight Hawk[/B][/COLOR][COLOR=white] Wizard[/COLOR]","Updating",'', 'Please Wait')
            addonPath=xbmcaddon.Addon(id=AddonID).getAddonInfo('path'); addonPath=xbmc.translatePath(addonPath); 
            xbmcPath=os.path.join(addonPath,"..",".."); xbmcPath=os.path.abspath(xbmcPath); failed=False  
            try:
                for root, dirs, files in os.walk(UPDATEPATH, topdown=True):
                    dirs[:] = [d for d in dirs if d in UPDATELIST]
                    for name in files:
                        try: os.remove(os.path.join(root,name))
                        except: pass
                    for name in dirs:
                        try: shutil.rmtree(os.path.join(root,name))
                        except: pass
            except: pass
        REMOVE_EMPTY_FOLDERS()
        REMOVE_EMPTY_FOLDERS()
        REMOVE_EMPTY_FOLDERS()
        REMOVE_EMPTY_FOLDERS()
        REMOVE_EMPTY_FOLDERS()
        REMOVE_EMPTY_FOLDERS()
        REMOVE_EMPTY_FOLDERS()
	UPDATEUSERDATA()
	
       
def UPDATEUSERDATA():
    linkupdate = OPEN_URL('https://archive.org/download/release_wizard/update_wizard.txt').replace('\n','').replace('\r','')
    matchupdate = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(linkupdate)
    if not matchupdate:
	dialog = xbmcgui.Dialog()
        dialog.ok('[COLOR=lime][B]knight hawk[/B][/COLOR][COLOR=white] Wizard[/COLOR]','NO Updates Currently Available','check back later.','')
	INDEX()           
    else:
        choice = xbmcgui.Dialog().yesno("UPDATING USERDATA", 'Do you want to update your Addon Settings?', '', 'Obsolete Addon Settings will be removed!', yeslabel='Yes',nolabel='No')
        if choice == 0:
            return
        elif choice == 1:
            dp.create("[COLOR=lime][B]knight hawk[/B][/COLOR][COLOR=white] Wizard[/COLOR]","Updating",'', 'Please Wait')
            addonPath=xbmcaddon.Addon(id=AddonID).getAddonInfo('path'); addonPath=xbmc.translatePath(addonPath); 
            xbmcPath=os.path.join(addonPath,"..",".."); xbmcPath=os.path.abspath(xbmcPath); failed=False  
            try:
                for root, dirs, files in os.walk(UPDATEADPATH, topdown=True):
                    dirs[:] = [d for d in dirs if d in UPDATELIST]
                    for name in files:
                        try: os.remove(os.path.join(root,name))
                        except: pass
                    for name in dirs:
                        try: shutil.rmtree(os.path.join(root,name))
                        except: pass
            except: pass
        REMOVE_EMPTY_FOLDERS()
        REMOVE_EMPTY_FOLDERS()
        REMOVE_EMPTY_FOLDERS()
        REMOVE_EMPTY_FOLDERS()
        REMOVE_EMPTY_FOLDERS()
        REMOVE_EMPTY_FOLDERS()
        REMOVE_EMPTY_FOLDERS()
	dialog = xbmcgui.Dialog()
	dialog.ok('[COLOR=lime][B]knight hawk[/B][/COLOR][COLOR=white] Wizard[/COLOR]','Addons Cleaned Now Install The Update from knight hawk Builds','','')
	UPDATEMENU()
	
	
def WIZARDCHECK():
    linkupdate = OPEN_URL('https://archive.org/download/release_wizard/update_wizard.txt').replace('\n','').replace('\r','')
    matchupdate = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(linkupdate)
    if not matchupdate:
		dialog = xbmcgui.Dialog()
		dialog.ok('[COLOR=lime][B]knight hawk[/B][/COLOR][COLOR=white] Wizard[/COLOR]','NO Updates Currently Available','check back later.','')
		INDEX()
    WIZARDUPDATE()	
    
	
def WIZARDUPDATE():
    linkupdate = OPEN_URL('https://archive.org/download/release_wizard/update_wizard.txt').replace('\n','').replace('\r','')
    matchupdate = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(linkupdate)
    # if skin!= "skin.confluence":
	# dialog = xbmcgui.Dialog()
        # dialog.ok('[COLOR=lime][B]SchisM TV[/B][/COLOR][COLOR=white] Updater[/COLOR] ','Please switch to the default Confluence skin','before proceeding.','')
        # xbmc.executebuiltin("ActivateWindow(appearancesettings)")
        # return
    
	
	
    path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
    dp = xbmcgui.DialogProgress()
    dp.create("[COLOR=lime][B]knight hawk[/B][/COLOR][COLOR=white] Updater[/COLOR]","Downloading Update",'', 'Please Wait')
    for name,url,iconimage,fanart,description in matchupdate:
		lib=os.path.join(path, name+'.zip')
    try:
       os.remove(lib)
    except:
       pass
    for name,url,iconimage,fanart,description in matchupdate:
            downloader.download(url, lib, dp)
    addonfolder = xbmc.translatePath(os.path.join('special://','home'))
    time.sleep(2)
    dp.update(0,"", "Extracting Zip Please Wait")
    print '======================================='
    print addonfolder
    print '======================================='
    extract.all(lib,addonfolder,dp)
    dialog = xbmcgui.Dialog()
    dialog.ok("[COLOR=lime][B]knight hawk[/B][/COLOR][COLOR=white] Updater[/COLOR]", "To save changes you now need to force close Kodi, DO not Forget to Clear Packages After Restart ... Press OK to force close Kodi")
    killxbmc()
def killxbmc():
    choice = xbmcgui.Dialog().yesno('Force Close XBMC/Kodi', 'We will now attempt to force close Kodi, this is', 'to be used if having problems with guisettings.xml', 'sticking. Would you like to continue?', nolabel='No, Cancel',yeslabel='Yes, Close')
    if choice == 0:
        INDEX()
    elif choice == 1:
        pass
    myplatform = platform()
    print "Platform: " + str(myplatform)
    if myplatform == 'osx': # OSX
        print "############   try osx force close  #################"
        try: os.system('killall -9 XBMC')
        except: pass
        try: os.system('killall -9 Kodi')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.",'')
    elif myplatform == 'linux': #Linux
        print "############   try linux force close  #################"
        try: os.system('killall XBMC')
        except: pass
        try: os.system('killall Kodi')
        except: pass
        try: os.system('killall -9 xbmc.bin')
        except: pass
        try: os.system('killall -9 kodi.bin')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.",'')
    elif myplatform == 'android': # Android  
        print "############   try android force close  #################"
        try: os.system('adb shell am force-stop org.xbmc.kodi')
        except: pass
        try: os.system('adb shell am force-stop org.kodi')
        except: pass
        try: os.system('adb shell am force-stop org.xbmc.xbmc')
        except: pass
        try: os.system('adb shell am force-stop org.xbmc')
        except: pass        
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "Your system has been detected as Android, you ", "[COLOR=yellow][B]MUST[/COLOR][/B] force close XBMC/Kodi. [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.","Pulling the power cable is the simplest method to force close.")
    elif myplatform == 'windows': # Windows
        print "############   try windows force close  #################"
        try:
            os.system('@ECHO off')
            os.system('tskill XBMC.exe')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('tskill Kodi.exe')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('TASKKILL /im Kodi.exe /f')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('TASKKILL /im XBMC.exe /f')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.","Use task manager and NOT ALT F4")
    else: #ATV
        print "############   try atv force close  #################"
        try: os.system('killall AppleTV')
        except: pass
        print "############   try raspbmc force close  #################" #OSMC / Raspbmc
        try: os.system('sudo initctl stop kodi')
        except: pass
        try: os.system('sudo initctl stop xbmc')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit via the menu.","Your platform could not be detected so just pull the power cable.")

def Addon_Settings():
    ADDON.openSettings(sys.argv[0])

def WipeXBMC():
    if skin!= "skin.confluence":
        dialog.ok('[COLOR=blue][B]knight hawk[/B][/COLOR][COLOR=green][/COLOR] Custom Builds Tool','Please switch to the default Confluence skin','before performing a wipe.','')
        xbmc.executebuiltin("ActivateWindow(appearancesettings)")
        return
    else:
        choice = xbmcgui.Dialog().yesno("VERY IMPORTANT", 'This will completely wipe your install.', 'Would you like to create a backup before proceeding?', '', yeslabel='Yes',nolabel='No')
        if choice == 1:
            mybackuppath = xbmc.translatePath(os.path.join(backupdir,'knighthawk Builds','My Builds'))
            if not os.path.exists(mybackuppath):
                os.makedirs(mybackuppath)
            vq = _get_keyboard( heading="Enter a name for this backup" )
            if ( not vq ): return False, 0
            title = urllib.quote_plus(vq)
            backup_zip = xbmc.translatePath(os.path.join(mybackuppath,title+'.zip'))
            exclude_dirs_full =  ['backupdir','plugin.video.knighthawk','repository.knighthawk.addons']
            exclude_files_full = ["xbmc.log","xbmc.old.log","kodi.log","kodi.old.log",'.DS_Store','.setup_complete','XBMCHelper.conf']
            message_header = "Creating full backup of existing build"
            message1 = "Archiving..."
            message2 = ""
            message3 = "Please Wait"
            ARCHIVE_CB(HOME, backup_zip, message_header, message1, message2, message3, exclude_dirs_full, exclude_files_full)
    choice2 = xbmcgui.Dialog().yesno("ABSOLUTELY CERTAIN?!!!", 'Are you absolutely certain you want to wipe this install?', '', 'All addons EXCLUDING THIS WIZARD will be completely wiped!', yeslabel='Yes',nolabel='No')
    if choice2 == 0:
        return
    elif choice2 == 1:
        dp.create("[COLOR=blue][B]knight hawk[/B][/COLOR] Custom Builds Tool","Wiping Install",'', 'Please Wait')
        try:
            for root, dirs, files in os.walk(HOME,topdown=True):
                dirs[:] = [d for d in dirs if d not in EXCLUDES]
                for name in files:
                    try:
                        os.remove(os.path.join(root,name))
                        os.rmdir(os.path.join(root,name))
                    except: pass
                        
                for name in dirs:
                    try: os.rmdir(os.path.join(root,name)); os.rmdir(root)
                    except: pass
        except: pass
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    dialog.ok('[COLOR=blue][B]knight hawk [/B][/COLOR] Custom Builds Tool','Wipe Successful, please restart XBMC/Kodi for changes to take effect.','','')

def REMOVE_EMPTY_FOLDERS():

    print"########### Start Removing Empty Folders #########"
    empty_count = 0
    used_count = 0
    for curdir, subdirs, files in os.walk(HOME):
        if len(subdirs) == 0 and len(files) == 0: #check for empty directories. len(files) == 0 may be overkill
            empty_count += 1 #increment empty_count
            os.rmdir(curdir) #delete the directory
            print "successfully removed: "+curdir
        elif len(subdirs) > 0 and len(files) > 0: #check for used directories
            used_count += 1 #increment used_count
#---------------------------------------------------------------------------------------------------
#Function to do a full wipe - this is called when doing a fresh CB install.
#Thanks to kozz for working out how to add an exclude clause so AMObox Custom Builds addon_data and addon isn't touched.
def WipeInstall():
    if skin!= "skin.confluence":
        dialog.ok('[COLOR=blue][B]knighthawk[/B][/COLOR][COLOR=green]box[/COLOR] Tool','Please switch to the default Confluence skin','before performing a wipe.','')
        xbmc.executebuiltin("ActivateWindow(appearancesettings)")       
    else:
        choice = xbmcgui.Dialog().yesno("WANT TO CONTINUE?", 'Are you absolutely certain you want to wipe this install?', '', 'All addons EXCLUDING THIS WIZARD will be completely wiped!', yeslabel='Yes',nolabel='No')
        if choice == 0:
            return
        elif choice == 1:
            dp.create("[COLOR=blue][B]knighthawk[/B][/COLOR][COLOR=green]box[/COLOR] Custom Builds Tool","Wiping Install",'', 'Please Wait')
            addonPath=xbmcaddon.Addon(id=AddonID).getAddonInfo('path'); addonPath=xbmc.translatePath(addonPath); 
            xbmcPath=os.path.join(addonPath,"..",".."); xbmcPath=os.path.abspath(xbmcPath); failed=False  
            try:
                for root, dirs, files in os.walk(xbmcPath,topdown=True):
                    dirs[:] = [d for d in dirs if d not in EXCLUDES]
                    for name in files:
                        try: os.remove(os.path.join(root,name))
                        except: pass
                    for name in dirs:
                        try: os.rmdir(os.path.join(root,name))
                        except: pass
            except: pass
        REMOVE_EMPTY_FOLDERS()
        REMOVE_EMPTY_FOLDERS()
        REMOVE_EMPTY_FOLDERS()
        REMOVE_EMPTY_FOLDERS()
        REMOVE_EMPTY_FOLDERS()
        REMOVE_EMPTY_FOLDERS()
        REMOVE_EMPTY_FOLDERS()

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param

def addDirectoryItem(handle, url, listitem, isFolder):
    xbmcplugin.addDirectoryItem(handle, url, listitem, isFolder)

def addBuildDir(name,url,mode,iconimage,fanart,video,description,skins,guisettingslink):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&video="+urllib.quote_plus(video)+"&description="+urllib.quote_plus(description)+"&skins="+urllib.quote_plus(skins)+"&guisettingslink="+urllib.quote_plus(guisettingslink)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        liz.setProperty( "Build.Video", video )
        if (mode==None) or (mode=='restore_option') or (mode=='backup_option') or (mode=='cb_root_menu') or (mode=='genres') or (mode=='grab_builds') or (mode=='community_menu') or (mode=='instructions') or (mode=='countries')or (url==None) or (len(url)<1):
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        else:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok

def platform():
    if xbmc.getCondVisibility('system.platform.android'):
        return 'android'
    elif xbmc.getCondVisibility('system.platform.linux'):
        return 'linux'
    elif xbmc.getCondVisibility('system.platform.windows'):
        return 'windows'
    elif xbmc.getCondVisibility('system.platform.osx'):
        return 'osx'
    elif xbmc.getCondVisibility('system.platform.atv2'):
        return 'atv2'
    elif xbmc.getCondVisibility('system.platform.ios'):
        return 'ios'
#---------------------------------------------------------------------------------------------------
# Addon starts here
params=get_params()
url=None
name=None
buildname=None
updated=None
author=None
version=None
mode=None
iconimage=None
description=None
video=None
link=None
skins=None
videoaddons=None
audioaddons=None
programaddons=None
audioaddons=None
sources=None
local=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        guisettingslink=urllib.unquote_plus(params["guisettingslink"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:
        fanart=urllib.unquote_plus(params["fanart"])
except:
        pass
try:        
        mode=str(params["mode"])
except:
        pass
try:
        link=urllib.unquote_plus(params["link"])
except:
        pass
try:
        skins=urllib.unquote_plus(params["skins"])
except:
        pass
try:
        videoaddons=urllib.unquote_plus(params["videoaddons"])
except:
        pass
try:
        audioaddons=urllib.unquote_plus(params["audioaddons"])
except:
        pass
try:
        programaddons=urllib.unquote_plus(params["programaddons"])
except:
        pass
try:
        pictureaddons=urllib.unquote_plus(params["pictureaddons"])
except:
        pass
try:
        local=urllib.unquote_plus(params["local"])
except:
        pass
try:
        sources=urllib.unquote_plus(params["sources"])
except:
        pass
try:
        adult=urllib.unquote_plus(params["adult"])
except:
        pass
try:
        buildname=urllib.unquote_plus(params["buildname"])
except:
        pass
try:
        updated=urllib.unquote_plus(params["updated"])
except:
        pass
try:
        version=urllib.unquote_plus(params["version"])
except:
        pass
try:
        author=urllib.unquote_plus(params["author"])
except:
        pass
try:        
        description=urllib.unquote_plus(params["description"])
except:
        pass
try:        
        video=urllib.unquote_plus(params["video"])
except:
        pass

 


def WIZARD(name,url,description):
    if skin!= "skin.confluence":
	dialog = xbmcgui.Dialog()
        dialog.ok('[COLOR=lime][B]knighthawk[/B][/COLOR][COLOR=white]  Wizard[/COLOR] ','Please switch to the default Confluence skin','before proceeding.','')
        xbmc.executebuiltin("ActivateWindow(appearancesettings)")
        return
    path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
    dp = xbmcgui.DialogProgress()
    dp.create("[COLOR=lime][B]knighthawk[/B][/COLOR][COLOR=white] Wizard[/COLOR]","Downloading ",'', 'Please Wait')
    lib=os.path.join(path, name+'.zip')
    try:
       os.remove(lib)
    except:
       pass
	
    downloader.download(url, lib, dp)
    addonfolder = xbmc.translatePath(os.path.join('special://','home'))
    time.sleep(2)
    dp.update(0,"", "Extracting Zip Please Wait")
    print '======================================='
    print addonfolder
    print '======================================='
    extract.all(lib,addonfolder,dp)
    dialog = xbmcgui.Dialog()
    dialog.ok("[COLOR=lime][B]knighthawk[/B][/COLOR][COLOR=white] Wizard[/COLOR]", "To save changes you now need to force close Kodi, Press OK to force close Kodi")
    
    killxbmc()


def WIZARDUNLOCK(name,url,description):
    url = "https://archive.org/download/wizard_rel/unlockbuild.zip"
    path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
    dp = xbmcgui.DialogProgress()
    dp.create("[COLOR=lime][B]knighthawk[/B][/COLOR][COLOR=white] Wizard[/COLOR]","Downloading ",'', 'Please Wait')
    lib=os.path.join(path,'unlockbuild.zip')
    try:
       os.remove(lib)
    except:
       pass
	
    downloader.download(url, lib, dp)
    addonfolder = xbmc.translatePath(os.path.join('special://','home'))
    time.sleep(2)
    dp.update(0,"", "Extracting Zip Please Wait")
    print '======================================='
    print addonfolder
    print '======================================='
    extract.all(lib,addonfolder,dp)
    dialog = xbmcgui.Dialog()
    dialog.ok("[COLOR=lime][B]knighthawk[/B][/COLOR][COLOR=white] Wizard[/COLOR]", "To save changes you now need to force close Kodi, Press OK to force close Kodi")
    
    killxbmc()
################################
###DELETE PACKAGES##############
####THANKS GUYS @ XUNITY########

def DeletePackages(url):
    print '############################################################       DELETING PACKAGES             ###############################################################'
    packages_cache_path = xbmc.translatePath(os.path.join('special://home/addons/packages', ''))
    try:    
        for root, dirs, files in os.walk(packages_cache_path):
            file_count = 0
            file_count += len(files)
            
        # Count files and give option to delete
            if file_count > 0:
    
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete Package Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
                            
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                    dialog = xbmcgui.Dialog()
                    dialog.ok("[COLOR lime][B]knighthawk[/B][/COLOR][COLOR white]Wizard[/COLOR]", "Packages Successfuly Removed", "")
    except: 
        dialog = xbmcgui.Dialog()
        dialog.ok("[COLOR lime][B]knighthawk[/B][/COLOR][COLOR white]Wizard[/COLOR]", "Sorry we were not able to remove Package Files", "")
    
#################################
###DELETE CACHE##################
####THANKS GUYS @ XUNITY########
	
def deletecachefiles(url):
    print '############################################################       DELETING STANDARD CACHE             ###############################################################'
    xbmc_cache_path = os.path.join(xbmc.translatePath('special://home'), 'cache')
    if os.path.exists(xbmc_cache_path)==True:    
        for root, dirs, files in os.walk(xbmc_cache_path):
            file_count = 0
            file_count += len(files)
        
        # Count files and give option to delete
            if file_count > 0:
    
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
                
                    for f in files:
                        try:
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                        
            else:
                pass
    if xbmc.getCondVisibility('system.platform.ATV2'):
        atv2_cache_a = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other')
        
        for root, dirs, files in os.walk(atv2_cache_a):
            file_count = 0
            file_count += len(files)
        
            if file_count > 0:

                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete ATV2 Cache Files", str(file_count) + " files found in 'Other'", "Do you want to delete them?"):
                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass
        atv2_cache_b = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'LocalAndRental')
        
        for root, dirs, files in os.walk(atv2_cache_b):
            file_count = 0
            file_count += len(files)
        
            if file_count > 0:

                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete ATV2 Cache Files", str(file_count) + " files found in 'LocalAndRental'", "Do you want to delete them?"):
                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass
              # Set path to Cydia Archives cache files
                             

    # Set path to What th Furk cache files
    wtf_cache_path = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.whatthefurk/cache'), '')
    if os.path.exists(wtf_cache_path)==True:    
        for root, dirs, files in os.walk(wtf_cache_path):
            file_count = 0
            file_count += len(files)
        
        # Count files and give option to delete
            if file_count > 0:
    
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete WTF Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass
                
                # Set path to 4oD cache files
    channel4_cache_path= os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.4od/cache'), '')
    if os.path.exists(channel4_cache_path)==True:    
        for root, dirs, files in os.walk(channel4_cache_path):
            file_count = 0
            file_count += len(files)
        
        # Count files and give option to delete
            if file_count > 0:
    
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete 4oD Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass
                
                # Set path to BBC iPlayer cache files
    iplayer_cache_path= os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.iplayer/iplayer_http_cache'), '')
    if os.path.exists(iplayer_cache_path)==True:    
        for root, dirs, files in os.walk(iplayer_cache_path):
            file_count = 0
            file_count += len(files)
        
        # Count files and give option to delete
            if file_count > 0:
    
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete BBC iPlayer Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass
                
                
                # Set path to Simple Downloader cache files
    downloader_cache_path = os.path.join(xbmc.translatePath('special://profile/addon_data/script.module.simple.downloader'), '')
    if os.path.exists(downloader_cache_path)==True:    
        for root, dirs, files in os.walk(downloader_cache_path):
            file_count = 0
            file_count += len(files)
        
        # Count files and give option to delete
            if file_count > 0:
    
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete Simple Downloader Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass
                
                # Set path to ITV cache files
    itv_cache_path = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.itv/Images'), '')
    if os.path.exists(itv_cache_path)==True:    
        for root, dirs, files in os.walk(itv_cache_path):
            file_count = 0
            file_count += len(files)
        
        # Count files and give option to delete
            if file_count > 0:
    
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete ITV Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass
				
                # Set path to temp cache files
    temp_cache_path = os.path.join(xbmc.translatePath('special://home/temp'), '')
    if os.path.exists(temp_cache_path)==True:    
        for root, dirs, files in os.walk(temp_cache_path):
            file_count = 0
            file_count += len(files)
        
        # Count files and give option to delete
            if file_count > 0:
    
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete TEMP dir Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass
				

    dialog = xbmcgui.Dialog()
    dialog.ok("[COLOR blue][B]AMO[/B][/COLOR][COLOR green][B]box[/B][/COLOR] [COLOR white]Wizard[/COLOR]", " All Cache Files Removed", "[COLOR yellow]Brought To You By [COLOR blue][B]AMO[/B][/COLOR][COLOR green][B]box[/B][/COLOR][/COLOR]")
 
        
def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link

###############################################################
###FORCE CLOSE KODI - ANDROID ONLY WORKS IF ROOTED#############
#######LEE @ COMMUNITY BUILDS##################################

def killxbmc():
    choice = xbmcgui.Dialog().yesno('[COLOR=green]Force Close Kodi[/COLOR]', 'You are about to close Kodi', 'Would you like to continue?', nolabel='No, Cancel',yeslabel='[COLOR=green]Yes, Close[/COLOR]')
    if choice == 0:
        return
    elif choice == 1:
        pass
    myplatform = platform()
    print "Platform: " + str(myplatform)
    if myplatform == 'osx': # OSX
        print "############   try osx force close  #################"
        try: os.system('killall -9 XBMC')
        except: pass
        try: os.system('killall -9 Kodi')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.",'')
    elif myplatform == 'linux': #Linux
        print "############   try linux force close  #################"
        try: os.system('killall XBMC')
        except: pass
        try: os.system('killall Kodi')
        except: pass
        try: os.system('killall -9 xbmc.bin')
        except: pass
        try: os.system('killall -9 kodi.bin')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.",'')
    elif myplatform == 'android': # Android  
        print "############   try android force close  #################"
        try: os.system('adb shell am force-stop org.xbmc.kodi')
        except: pass
        try: os.system('adb shell am force-stop org.kodi')
        except: pass
        try: os.system('adb shell am force-stop org.xbmc.xbmc')
        except: pass
        try: os.system('adb shell am force-stop org.xbmc')
        except: pass        
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "Your system has been detected as Android, you ", "[COLOR=yellow][B]MUST[/COLOR][/B] force close XBMC/Kodi. [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.","Pulling the power cable is the simplest method to force close.")
    elif myplatform == 'windows': # Windows
        print "############   try windows force close  #################"
        try:
            os.system('@ECHO off')
            os.system('tskill XBMC.exe')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('tskill Kodi.exe')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('TASKKILL /im Kodi.exe /f')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('TASKKILL /im XBMC.exe /f')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.","Use task manager and NOT ALT F4")
    else: #ATV
        print "############   try atv force close  #################"
        try: os.system('killall AppleTV')
        except: pass
        print "############   try raspbmc force close  #################" #OSMC / Raspbmc
        try: os.system('sudo initctl stop kodi')
        except: pass
        try: os.system('sudo initctl stop xbmc')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit via the menu.","Your platform could not be detected so just pull the power cable.")    

##########################
###DETERMINE PLATFORM#####
##########################
        
def platform():
    if xbmc.getCondVisibility('system.platform.android'):
        return 'android'
    elif xbmc.getCondVisibility('system.platform.linux'):
        return 'linux'
    elif xbmc.getCondVisibility('system.platform.windows'):
        return 'windows'
    elif xbmc.getCondVisibility('system.platform.osx'):
        return 'osx'
    elif xbmc.getCondVisibility('system.platform.atv2'):
        return 'atv2'
    elif xbmc.getCondVisibility('system.platform.ios'):
        return 'ios'
    
############################
###FRESH START##############
############################

def FRESHSTART(params):
    if skin!= "skin.confluence":
        dialog.ok('[COLOR lime][B]knighthawk[/B][/COLOR][COLOR white]Wizard[/COLOR] ','Please switch to the default Confluence skin','before performing a wipe.','')
        xbmc.executebuiltin("ActivateWindow(appearancesettings)")
        return
    else:
        choice2 = xbmcgui.Dialog().yesno("[COLOR=red]ABSOLUTELY CERTAIN?!!![/COLOR]", 'Are you absolutely certain you want to wipe this install?', '', 'All addons EXCLUDING THIS WIZARD will be completely wiped!', yeslabel='[COLOR=red]Yes[/COLOR]',nolabel='[COLOR=green]No[/COLOR]')
    if choice2 == 0:
        return
    elif choice2 == 1:
        dp.create("[COLOR lime][B]knighthawk[/B][/COLOR][COLOR white]Wizard[/COLOR]","Wiping Install",'', 'Please Wait')
        try:
            for root, dirs, files in os.walk(HOME,topdown=True):
                dirs[:] = [d for d in dirs if d not in EXCLUDES]
                for name in files:
                    try:
                        os.remove(os.path.join(root,name))
                        os.rmdir(os.path.join(root,name))
                    except: pass
                        
                for name in dirs:
                    try: os.rmdir(os.path.join(root,name)); os.rmdir(root)
                    except: pass
        except: pass
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    dialog.ok('[COLOR lime][B]knighthawk[/B][/COLOR][COLOR white]Wizard[/COLOR]','Wipe Successful, please restart XBMC/Kodi for changes to take effect.','','')
    killxbmc()

def REMOVE_EMPTY_FOLDERS():
#initialize the counters
    print"########### Start Removing Empty Folders #########"
    empty_count = 0
    used_count = 0
    for curdir, subdirs, files in os.walk(HOME):
        if len(subdirs) == 0 and len(files) == 0: #check for empty directories. len(files) == 0 may be overkill
            empty_count += 1 #increment empty_count
            os.rmdir(curdir) #delete the directory
            print "successfully removed: "+curdir
        elif len(subdirs) > 0 and len(files) > 0: #check for used directories
            used_count += 1 #increment used_count
#---------------------------------------------------------------------------------------------------

	
      
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param

N = base64.decodestring('')
T = base64.decodestring('L2FkZG9ucy50eHQ=')
B = base64.decodestring('')
F = base64.decodestring('')

def addDir(name,url,mode,iconimage,fanart,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        if mode==90 :
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        else:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

        
                      
params=get_params()
url=None
name=None
mode=None
iconimage=None
fanart=None
description=None


try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        mode=int(params["mode"])
except:
        pass
try:        
        fanart=urllib.unquote_plus(params["fanart"])
except:
        pass
try:        
        description=urllib.unquote_plus(params["description"])
except:
        pass
        
        
print str(PATH)+': '+str(VERSION)
print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IconImage: "+str(iconimage)


def setView(content, viewType):
    # set content type so library shows more views and info
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    if ADDON.getSetting('auto-view')=='true':
        xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )
        
        
if mode==None or url==None or len(url)<1:
        INDEX()
elif mode==1:
        UPDATEMENU()	
elif mode==20:
        BUILDMENU()
elif mode==2:
        UPDATER()
elif mode==4:
        RESTORE()
		
elif mode==3:
        BACKUPMENU()

		
elif mode==6:        
	FRESHSTART(params)
	
elif mode==7:
       DeletePackages(url)

		
elif mode==10:
        ADDONWIZARD(name,url,description)

elif mode==82:
        print "############   WIPE XBMC   #################"
        WipeXBMC()

elif mode==85:
        print "############   ATTEMPT TO KILL XBMC/KODI   #################"
        killxbmc()
		
elif mode==83:
        print "############   FIX SPECIAL PATHS   #################"
        FIX_SPECIAL(url)
		
elif mode==90:
        WIZARD(name,url,description)

elif mode==11:
        WIZARDUNLOCK(name,url,description)	
xbmcplugin.endOfDirectory(int(sys.argv[1]))

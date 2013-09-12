import urllib,urllib2,re,cookielib,sys,os
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
from resources.libs import main

#Mash Up - by Mash2k3 2012.

from t0mm0.common.addon import Addon
addon_id = 'plugin.video.movie25'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon('plugin.video.movie25', sys.argv)
art = main.art
from universal import watchhistory    
wh = watchhistory.WatchHistory('plugin.video.movie25')
try:
    import json
except:
    import simplejson as json
datapath = addon.get_profile()
CustomChannel=os.path.join(datapath,'XmlChannels')

try:
    os.makedirs(CustomChannel)
except:
    pass
PlaylistFile=os.path.join(CustomChannel,'PlaylistFile')
FolderFile=os.path.join(CustomChannel,'FolderFile')

if selfAddon.getSetting("artbrowser") == "0":
    browseType='files'
if selfAddon.getSetting("artbrowser") == "1":
    browseType='programs'



def MAIN():
    folders='home'
    pl=0
    fl=0
    if selfAddon.getSetting("hideinstruction") == "false":
        main.addPlayc('My XML Channel Instructions','nills',248,art+'/xml.png','','','','','')
    if selfAddon.getSetting("addmethod") == "false":
        main.addPlayc('Add Playlist',folders,250,art+'/xmlplaylistadd.png','','','','','')
        main.addPlayc('Add Folder',folders,252,art+'/folderadd.png','','','','','')
    if os.path.exists(PlaylistFile):
        playlist=re.compile("{'thumb': '(.*?)', 'title': '(.*?)', 'url': '(.*?)', 'fanart': '(.*?)', 'folder': '(.*?)', 'typeXml': '(.*?)'}").findall(open(PlaylistFile,'r').read())
        for thumb,name,url,fanart,folder,typeXml in sorted(playlist):
            if urllib.unquote_plus(folders)==urllib.unquote_plus(folder):
                name=urllib.unquote_plus(name)
                url=urllib.unquote_plus(url)
                thumb=urllib.unquote_plus(thumb)
                fanart=urllib.unquote_plus(fanart)
                if typeXml =='MashUp':
                    main.addDirXml(name,url,239,thumb,folders,fanart,'','','')
                else:
                    main.addDirXml(name,url,257,thumb,folders,fanart,typeXml,'','')
                pl=pl+1
    if os.path.exists(FolderFile):
        foldered=re.compile("{'fanart': '(.*?)', 'folder': '(.*?)', 'thumb': '(.*?)', 'title': '(.*?)'}").findall(open(FolderFile,'r').read())
        for fanart,folder,thumb,name in sorted(foldered):
            if urllib.unquote_plus(folders)==urllib.unquote_plus(folder):
                name=urllib.unquote_plus(name)
                folder=urllib.unquote_plus(folder)
                thumb=urllib.unquote_plus(thumb)
                fanart=urllib.unquote_plus(fanart)
                main.addXmlFolder(name,folder+'-'+name,253,thumb,folder,fanart,'','','')
                fl=fl+1
    if fl==0 and pl==0 and selfAddon.getSetting("addmethod") == "true":
        main.addPlayc('Add Playlist',folders,250,art+'/xmlplaylistadd.png','','','','','')
        main.addPlayc('Add Folder',folders,252,art+'/folderadd.png','','','','','')

def XmlIns():
        dir = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.movie25/resources/message', ''))
        chlg = os.path.join(dir, 'xmlchannels.txt')
        main.TextBoxes("[B][COLOR red]MashUp XML Instructions![/B][/COLOR]",chlg)

def addPlaylist(folder):
    dialog = xbmcgui.Dialog()
    ret = dialog.select('[COLOR=FF67cc33][B]Choose Entry Type[/COLOR][/B]',['[B][COLOR=FF67cc33]Select a MashUp XML Using Filemanager[/COLOR][/B]','[B][COLOR=FF67cc33]Select a MashUp XML Using Set User Source[/COLOR][/B]','[B][COLOR=FF67cc33]Enter a MashUp XML URL[/COLOR][/B]','[B][COLOR yellow]Select a Livestreams XML Using Filemanager[/COLOR][/B]','[B][COLOR yellow]Select a Livestreams XML Using Set User Source[/COLOR][/B]','[B][COLOR yellow]Enter a Livestreams XML URL[/COLOR][/B]'])
    if ret == -1:
        return
    else:
        if ret == 0:
            xmlfile = xbmcgui.Dialog().browse(1, "[B][COLOR=FF67cc33]XML File Location[/COLOR][/B]", 'programs')
            typeXml='MashUp'
        if ret == 1:
            xmlfile = xbmcgui.Dialog().browse(1, "[B][COLOR=FF67cc33]XML File Location[/COLOR][/B]", 'files')
            typeXml='MashUp'
        if ret == 2:
            keyboard = xbmc.Keyboard('','[B][COLOR=FF67cc33]Enter XML URL[/COLOR][/B]')
            keyboard.doModal()
            if (keyboard.isConfirmed() == False):
                return
            xmlfile = keyboard.getText()
            typeXml='MashUp'
        if ret == 3:
            xmlfile = xbmcgui.Dialog().browse(1, "[B][COLOR=FF67cc33]XML File Location[/COLOR][/B]", 'programs')
            typeXml='Livestreams'
        if ret == 4:
            xmlfile = xbmcgui.Dialog().browse(1, "[B][COLOR=FF67cc33]XML File Location[/COLOR][/B]", 'files')
            typeXml='Livestreams'
        if ret == 5:
            keyboard = xbmc.Keyboard('','[B][COLOR=FF67cc33]Enter XML URL[/COLOR][/B]')
            keyboard.doModal()
            if (keyboard.isConfirmed() == False):
                return
            xmlfile = keyboard.getText()
            typeXml='Livestreams'
        if xmlfile:
            keyboard = xbmc.Keyboard('','[B][COLOR=FF67cc33]Enter Playlist Name[/COLOR][/B]')
            keyboard.doModal()
            if (keyboard.isConfirmed() == False):
                return
            else:
                name = keyboard.getText()
                if name != '':
                    
                    if ret == 1:
                        if selfAddon.getSetting("playlistthumb") == "true":
                            thumb = xbmcgui.Dialog().browse(2, "[B][COLOR=FF67cc33]Thumbnail File Location[/COLOR][/B]", 'files')
                        else:
                            thumb=''
                        if selfAddon.getSetting("playlistfanart") == "true":
                            fanart = xbmcgui.Dialog().browse(2, "[B][COLOR=FF67cc33]Fanart File Location[/COLOR][/B]", 'files')
                        else:
                            fanart=''
                    else:
                        if selfAddon.getSetting("playlistthumb") == "true":
                            thumb = xbmcgui.Dialog().browse(2, "[B][COLOR=FF67cc33]Thumbnail File Location[/COLOR][/B]", 'programs')
                        else:
                            thumb=''
                        if selfAddon.getSetting("playlistfanart") == "true":
                            fanart = xbmcgui.Dialog().browse(2, "[B][COLOR=FF67cc33]Fanart File Location[/COLOR][/B]", 'programs')
                        else:
                            fanart=''
                    
                    playlists = {}
                    playlists['title'] = urllib.quote_plus(name)
                    playlists['url'] = urllib.quote_plus(xmlfile)
                    playlists['thumb'] = urllib.quote_plus(thumb)
                    playlists['fanart'] = urllib.quote_plus(fanart)
                    playlists['folder'] = urllib.quote_plus(folder)
                    playlists['typeXml'] = urllib.quote_plus(typeXml)
                    if not os.path.exists(PlaylistFile):
                        open(PlaylistFile,'w').write(str(playlists))
                        xbmc.executebuiltin("XBMC.Notification([B][COLOR=FF67cc33]"+name+"[/COLOR][/B],[B]Playlist Created.[/B],3000,"")")
                    else:
                        open(PlaylistFile,'a').write(str(playlists))
                        xbmc.executebuiltin("XBMC.Notification([B][COLOR=FF67cc33]"+name+"[/COLOR][/B],[B]Playlist Created.[/B],3000,"")")
                    xbmc.executebuiltin("Container.Refresh")
                else:
                    xbmc.executebuiltin("XBMC.Notification([B][COLOR=FF67cc33]Sorry![/COLOR][/B],[B]Invalid entry[/B],3000,"")")
        return

def removePlaylist(title,murl,folders):
    if os.path.exists(PlaylistFile):
        playlist=re.compile("{'thumb': '(.*?)', 'title': '(.*?)', 'url': '(.*?)', 'fanart': '(.*?)', 'folder': '(.*?)', 'typeXml': '(.*?)'}").findall(open(PlaylistFile,'r').read())
        if len(playlist)<=1 and str(playlist).find(title):
            os.remove(PlaylistFile)
            xbmc.executebuiltin("Container.Refresh")
        if os.path.exists(PlaylistFile):
            for thumb,name,url,fanart,folder,typeXml in reversed (playlist):
                if title == urllib.unquote_plus(name) and urllib.unquote_plus(folders)==urllib.unquote_plus(folder):
                    playlist.remove((thumb,name,url,fanart,folder,typeXml))
                    os.remove(PlaylistFile)
                    for thumb,name,url,fanart,folder,typeXml in playlist:
                        try:
                            playlists = {}
                            playlists['title'] = name
                            playlists['url'] = url.replace('\\\\','\\')
                            playlists['thumb'] = thumb
                            playlists['fanart'] = fanart
                            playlists['folder'] = folder
                            playlists['typeXml'] = typeXml
                            open(PlaylistFile,'a').write(str(playlists))
                            xbmc.executebuiltin("Container.Refresh")
                            xbmc.executebuiltin("XBMC.Notification([B][COLOR=FF67cc33]"+title+"[/COLOR][/B],[B]Playlist Removed from Custom Channels[/B],4000,"")")
                        except: pass
        else: xbmc.executebuiltin("XBMC.Notification([B][COLOR green]Mash Up[/COLOR][/B],[B]You Have No Playlists[/B],1000,"")")
    return

def editFolder(title,folders):
    dialog = xbmcgui.Dialog()
    if selfAddon.getSetting("folderthumb") == "true" and selfAddon.getSetting("folderfanart") == "true":
        ret = dialog.select('[COLOR red][B]What Would you Like to Edit?[/COLOR][/B]',['[B][COLOR=FF67cc33]Folder Name[/COLOR][/B]','[B][COLOR=FF67cc33]Folder Thumbnail[/COLOR][/B]','[B][COLOR=FF67cc33]Folder Fanart[/COLOR][/B]'])
    if selfAddon.getSetting("folderthumb") == "true" and selfAddon.getSetting("folderfanart") == "false":
        ret = dialog.select('[COLOR red][B]What Would you Like to Edit?[/COLOR][/B]',['[B][COLOR=FF67cc33]Folder Name[/COLOR][/B]','[B][COLOR=FF67cc33]Folder Thumbnail[/COLOR][/B]'])
    if selfAddon.getSetting("folderthumb") == "false" and selfAddon.getSetting("folderfanart") == "true":
        ret = dialog.select('[COLOR red][B]What Would you Like to Edit?[/COLOR][/B]',['[B][COLOR=FF67cc33]Folder Name[/COLOR][/B]','[B][COLOR=FF67cc33]Folder Fanart[/COLOR][/B]'])
    if selfAddon.getSetting("folderthumb") == "false" and selfAddon.getSetting("folderfanart") == "false":
        ret = dialog.select('[COLOR red][B]What Would you Like to Edit?[/COLOR][/B]',['[B][COLOR=FF67cc33]Folder Name[/COLOR][/B]'])
    if ret == -1:
        return
    else:
        if ret == 0:
            playlists = {}
            keyboard = xbmc.Keyboard(title,'[B][COLOR=FF67cc33]Enter Folder Name[/COLOR][/B]')
            keyboard.doModal()
            if (keyboard.isConfirmed() == False):
                return
            else:
                newname = keyboard.getText()
                if newname != '':
                    
                    if os.path.exists(FolderFile):
                        foldered=re.compile("{'fanart': '(.*?)', 'folder': '(.+?)', 'thumb': '(.*?)', 'title': '(.+?)'}").findall(open(FolderFile,'r').read())
                        for fanart,folder,thumb,name in reversed (foldered):
                            if title == urllib.unquote_plus(name) and urllib.unquote_plus(folders)==urllib.unquote_plus(folder)+'-'+title:
                                foldered.remove((fanart,folder,thumb,name))
                                os.remove(FolderFile)
                                foldersDict = {}
                                foldersDict['title'] = urllib.quote_plus(newname)
                                foldersDict['thumb'] = thumb
                                foldersDict['fanart'] = fanart
                                foldersDict['folder'] = urllib.quote_plus(folder)
                                open(FolderFile,'a').write(str(foldersDict))
                                for fanart,folder,thumb,name in foldered:
                                        foldersDict['title'] = name
                                        foldersDict['thumb'] = thumb
                                        foldersDict['fanart'] = fanart
                                        foldersDict['folder'] = folder
                                        open(FolderFile,'a').write(str(foldersDict))
                                        xbmc.executebuiltin("XBMC.Notification([B][COLOR=FF67cc33]"+newname+"[/COLOR][/B],[B]Playlist Renamed[/B],4000,"")")
                                    #except: pass
                        
                        if os.path.exists(PlaylistFile):
                            playlist=re.compile("{'thumb': '(.*?)', 'title': '(.*?)', 'url': '(.*?)', 'fanart': '(.*?)', 'folder': '(.*?)', 'typeXml': '(.*?)'}").findall(open(PlaylistFile,'r').read())
                            for thumb,name,url,fanart,folder,typeXml in reversed (playlist):
                                if urllib.unquote_plus(folders)==urllib.unquote_plus(folder):
                                    newfolder='home-'+newname
                                    playlist.remove((thumb,name,url,fanart,folder,typeXml))
                                    os.remove(PlaylistFile)
                                    playlists['title'] = name
                                    playlists['url'] = url
                                    playlists['thumb'] = thumb
                                    playlists['fanart'] = fanart
                                    playlists['folder'] = newfolder
                                    playlists['typeXml'] = typeXml
                                    open(PlaylistFile,'a').write(str(playlists))
                                    for thumb,name,url,fanart,folder,typeXml in playlist:
                                        try:
                                        
                                            playlists['title'] = name
                                            playlists['url'] = url
                                            playlists['thumb'] = thumb
                                            playlists['fanart'] = fanart
                                            playlists['folder'] = folder
                                            playlists['typeXml'] = typeXml
                                            open(PlaylistFile,'a').write(str(playlists))
                                        except: pass
                        xbmc.executebuiltin("Container.Refresh")
        if ret == 1:
            newthumb = xbmcgui.Dialog().browse(2, "[B][COLOR=FF67cc33]Thumbnail File Location[/COLOR][/B]", browseType)
            if newthumb:
                    if os.path.exists(FolderFile):
                        foldered=re.compile("{'fanart': '(.*?)', 'folder': '(.+?)', 'thumb': '(.*?)', 'title': '(.+?)'}").findall(open(FolderFile,'r').read())
                        for fanart,folder,thumb,name in reversed (foldered):
                            if title == urllib.unquote_plus(name) and urllib.unquote_plus(folders)==urllib.unquote_plus(folder)+'-'+title:
                                foldered.remove((fanart,folder,thumb,name))
                                os.remove(FolderFile)
                                foldersDict = {}
                                foldersDict['title'] = name
                                foldersDict['thumb'] = urllib.quote_plus(newthumb)
                                foldersDict['fanart'] = fanart
                                foldersDict['folder'] = folder
                                open(FolderFile,'a').write(str(foldersDict))
                                for fanart,folder,thumb,name in foldered:
                                        foldersDict['title'] = name
                                        foldersDict['thumb'] = thumb
                                        foldersDict['fanart'] = fanart
                                        foldersDict['folder'] = folder
                                        open(FolderFile,'a').write(str(foldersDict))
                                        xbmc.executebuiltin("XBMC.Notification([B][COLOR=FF67cc33]"+newthumb+"[/COLOR][/B],[B]Folder Thumbnail Changed[/B],4000,"")")
                                xbmc.executebuiltin("Container.Refresh")
        if ret == 2:
            newfanart = xbmcgui.Dialog().browse(2, "[B][COLOR=FF67cc33]Fanart File Location[/COLOR][/B]", browseType)
            if newfanart:
                    if os.path.exists(FolderFile):
                        foldered=re.compile("{'fanart': '(.*?)', 'folder': '(.+?)', 'thumb': '(.*?)', 'title': '(.+?)'}").findall(open(FolderFile,'r').read())
                        for fanart,folder,thumb,name in reversed (foldered):
                            if title == urllib.unquote_plus(name) and urllib.unquote_plus(folders)==urllib.unquote_plus(folder)+'-'+title:
                                foldered.remove((fanart,folder,thumb,name))
                                os.remove(FolderFile)
                                foldersDict = {}
                                foldersDict['title'] = name
                                foldersDict['thumb'] = thumb
                                foldersDict['fanart'] = urllib.quote_plus(newfanart)
                                foldersDict['folder'] = folder
                                open(FolderFile,'a').write(str(foldersDict))
                                for fanart,folder,thumb,name in foldered:
                                        foldersDict['title'] = name
                                        foldersDict['thumb'] = thumb
                                        foldersDict['fanart'] = fanart
                                        foldersDict['folder'] = folder
                                        open(FolderFile,'a').write(str(foldersDict))
                                        xbmc.executebuiltin("XBMC.Notification([B][COLOR=FF67cc33]"+newfanart+"[/COLOR][/B],[B]Folder Fanart Changed[/B],4000,"")")
                                xbmc.executebuiltin("Container.Refresh")
                            
def editPlaylist(title,murl,folders):
    dialog = xbmcgui.Dialog()
    if selfAddon.getSetting("playlistthumb") == "true" and selfAddon.getSetting("playlistfanart") == "true":
        ret = dialog.select('[COLOR red][B]What Would you Like to Edit?[/COLOR][/B]',['[B][COLOR=FF67cc33]Playlist Name[/COLOR][/B]','[B][COLOR=FF67cc33]Playlist XML File[/COLOR][/B]','[B][COLOR=FF67cc33]Playlist Thumbnail[/COLOR][/B]','[B][COLOR=FF67cc33]Playlist Fanart[/COLOR][/B]'])
    if selfAddon.getSetting("playlistthumb") == "true" and selfAddon.getSetting("playlistfanart") == "false":
        ret = dialog.select('[COLOR red][B]What Would you Like to Edit?[/COLOR][/B]',['[B][COLOR=FF67cc33]Playlist Name[/COLOR][/B]','[B][COLOR=FF67cc33]Playlist XML File[/COLOR][/B]','[B][COLOR=FF67cc33]Playlist Thumbnail[/COLOR][/B]'])
    if selfAddon.getSetting("playlistthumb") == "false" and selfAddon.getSetting("playlistfanart") == "true":
        ret = dialog.select('[COLOR red][B]What Would you Like to Edit?[/COLOR][/B]',['[B][COLOR=FF67cc33]Playlist Name[/COLOR][/B]','[B][COLOR=FF67cc33]Playlist XML File[/COLOR][/B]','[B][COLOR=FF67cc33]Playlist Fanart[/COLOR][/B]'])
    if selfAddon.getSetting("playlistthumb") == "false" and selfAddon.getSetting("playlistfanart") == "false":
        ret = dialog.select('[COLOR red][B]What Would you Like to Edit?[/COLOR][/B]',['[B][COLOR=FF67cc33]Playlist Name[/COLOR][/B]','[B][COLOR=FF67cc33]Playlist XML File[/COLOR][/B]'])

    if ret == -1:
        return
    else:
        if ret == 0:
            playlists = {}
            keyboard = xbmc.Keyboard(title,'[B][COLOR=FF67cc33]Enter Playlist Name[/COLOR][/B]')
            keyboard.doModal()
            if (keyboard.isConfirmed() == False):
                return
            else:
                newname = keyboard.getText()
                if newname != '':
                    if os.path.exists(PlaylistFile):
                        playlist=re.compile("{'thumb': '(.*?)', 'title': '(.*?)', 'url': '(.*?)', 'fanart': '(.*?)', 'folder': '(.*?)', 'typeXml': '(.*?)'}").findall(open(PlaylistFile,'r').read())
                        for thumb,name,url,fanart,folder,typeXml in reversed (playlist):
                            if title == urllib.unquote_plus(name) and urllib.unquote_plus(folders)==urllib.unquote_plus(folder):
                                playlist.remove((thumb,name,url,fanart,folder,typeXml))
                                os.remove(PlaylistFile)
                                playlists['title'] = urllib.quote_plus(newname)
                                playlists['url'] = url
                                playlists['thumb'] = thumb
                                playlists['fanart'] = fanart
                                playlists['folder'] = folder
                                playlists['typeXml'] = typeXml
                                open(PlaylistFile,'a').write(str(playlists))
                                for thumb,name,url,fanart,folder,typeXml in playlist:
                                    try:
                                        
                                        playlists['title'] = name
                                        playlists['url'] = url
                                        playlists['thumb'] = thumb
                                        playlists['fanart'] = fanart
                                        playlists['folder'] = folder
                                        playlists['typeXml'] = typeXml
                                        open(PlaylistFile,'a').write(str(playlists))
                                        xbmc.executebuiltin("XBMC.Notification([B][COLOR=FF67cc33]"+newname+"[/COLOR][/B],[B]Playlist Renamed[/B],4000,"")")
                                    except: pass
                                xbmc.executebuiltin("Container.Refresh")
        if ret == 1:
            ret = dialog.select('[COLOR=FF67cc33][B]Choose Entry Type[/COLOR][/B]',['[B][COLOR=FF67cc33]Select a MashUp XML Using Filemanager[/COLOR][/B]','[B][COLOR=FF67cc33]Select a MashUp XML Using Set User Source[/COLOR][/B]','[B][COLOR=FF67cc33]Enter a MashUp XML URL[/COLOR][/B]','[B][COLOR yellow]Select a Livestreams XML Using Filemanager[/COLOR][/B]','[B][COLOR yellow]Select a Livestreams XML Using Set User Source[/COLOR][/B]','[B][COLOR yellow]Enter a Livestreams XML URL[/COLOR][/B]'])
            if ret == -1:
                return
            else:
                if ret == 0:
                    newxmlfile = xbmcgui.Dialog().browse(1, "[B][COLOR=FF67cc33]XML File Location[/COLOR][/B]", 'programs')
                    newtypeXml='MashUp'
                if ret == 1:
                    newxmlfile = xbmcgui.Dialog().browse(1, "[B][COLOR=FF67cc33]XML File Location[/COLOR][/B]", 'files')
                    newtypeXml='MashUp'
                if ret == 2:
                    keyboard = xbmc.Keyboard('','[B][COLOR=FF67cc33]Enter XML URL[/COLOR][/B]')
                    keyboard.doModal()
                    if (keyboard.isConfirmed() == False):
                        return
                    newxmlfile = keyboard.getText()
                    newtypeXml='MashUp'
                if ret == 3:
                    newxmlfile = xbmcgui.Dialog().browse(1, "[B][COLOR=FF67cc33]XML File Location[/COLOR][/B]", 'programs')
                    newtypeXml='Livestreams'
                if ret == 4:
                    newxmlfile = xbmcgui.Dialog().browse(1, "[B][COLOR=FF67cc33]XML File Location[/COLOR][/B]", 'files')
                    newtypeXml='Livestreams'
                if ret == 5:
                    keyboard = xbmc.Keyboard('','[B][COLOR=FF67cc33]Enter XML URL[/COLOR][/B]')
                    keyboard.doModal()
                    if (keyboard.isConfirmed() == False):
                        return
                    newxmlfile = keyboard.getText()
                    newtypeXml='Livestreams'
                if newxmlfile:
                    if newxmlfile != '':
                        playlists = {}
                        if os.path.exists(PlaylistFile):
                            playlist=re.compile("{'thumb': '(.*?)', 'title': '(.*?)', 'url': '(.*?)', 'fanart': '(.*?)', 'folder': '(.*?)', 'typeXml': '(.*?)'}").findall(open(PlaylistFile,'r').read())
                            for thumb,name,url,fanart,folder,typeXml in reversed (playlist):
                                if title == urllib.unquote_plus(name) and urllib.unquote_plus(folders)==urllib.unquote_plus(folder):
                                    playlist.remove((thumb,name,url,fanart,folder,typeXml))
                                    os.remove(PlaylistFile)
                                    playlists['title'] = name
                                    playlists['url'] = urllib.quote_plus(newxmlfile)
                                    playlists['thumb'] = thumb
                                    playlists['fanart'] = fanart
                                    playlists['folder'] = folder
                                    playlists['typeXml'] = urllib.quote_plus(newtypeXml)
                                    open(PlaylistFile,'a').write(str(playlists))
                                    for thumb,name,url,fanart,folder,typeXml in playlist:
                                        try:
                                        
                                            playlists['title'] = name
                                            playlists['url'] = url
                                            playlists['thumb'] = thumb
                                            playlists['fanart'] = fanart
                                            playlists['folder'] = folder
                                            playlists['typeXml'] = typeXml
                                            open(PlaylistFile,'a').write(str(playlists))
                                            xbmc.executebuiltin("XBMC.Notification([B][COLOR=FF67cc33]MashUp[/COLOR][/B],[B]Playlist XML Changed[/B],4000,"")")
                                        except: pass
                                    xbmc.executebuiltin("Container.Refresh")
        
        if ret == 2:
            newthumb = xbmcgui.Dialog().browse(2, "[B][COLOR=FF67cc33]Thumbnail File Location[/COLOR][/B]", browseType)
            if newthumb:
                        playlists = {}
                        if os.path.exists(PlaylistFile):
                            playlist=re.compile("{'thumb': '(.*?)', 'title': '(.*?)', 'url': '(.*?)', 'fanart': '(.*?)', 'folder': '(.*?)', 'typeXml': '(.*?)'}").findall(open(PlaylistFile,'r').read())
                            for thumb,name,url,fanart,folder,typeXml in reversed (playlist):
                                if title == urllib.unquote_plus(name) and urllib.unquote_plus(folders)==urllib.unquote_plus(folder):
                                    playlist.remove((thumb,name,url,fanart,folder,typeXml))
                                    os.remove(PlaylistFile)
                                    playlists['title'] = name
                                    playlists['url'] = url
                                    playlists['thumb'] = newthumb
                                    playlists['fanart'] = fanart
                                    playlists['folder'] = folder
                                    playlists['typeXml'] = typeXml
                                    open(PlaylistFile,'a').write(str(playlists))
                                    for thumb,name,url,fanart,folder,typeXml in playlist:
                                        try:
                                        
                                            playlists['title'] = name
                                            playlists['url'] = url
                                            playlists['thumb'] = thumb
                                            playlists['fanart'] = fanart
                                            playlists['folder'] = folder
                                            playlists['typeXml'] = typeXml
                                            open(PlaylistFile,'a').write(str(playlists))
                                            xbmc.executebuiltin("XBMC.Notification([B][COLOR=FF67cc33]MashUp[/COLOR][/B],[B]Playlist Thumbnail Changed[/B],4000,"")")
                                        except: pass
                                    xbmc.executebuiltin("Container.Refresh")
        if ret == 3:
            newfanart = xbmcgui.Dialog().browse(2, "[B][COLOR=FF67cc33]Fanart File Location[/COLOR][/B]", browseType)
            if newfanart:
                        playlists = {}
                        if os.path.exists(PlaylistFile):
                            playlist=re.compile("{'thumb': '(.*?)', 'title': '(.*?)', 'url': '(.*?)', 'fanart': '(.*?)', 'folder': '(.*?)', 'typeXml': '(.*?)'}").findall(open(PlaylistFile,'r').read())
                            for thumb,name,url,fanart,folder,typeXml in reversed (playlist):
                                if title == urllib.unquote_plus(name) and urllib.unquote_plus(folders)==urllib.unquote_plus(folder):
                                    playlist.remove((thumb,name,url,fanart,folder,typeXml))
                                    os.remove(PlaylistFile)
                                    playlists['title'] = name
                                    playlists['url'] = url
                                    playlists['thumb'] = thumb
                                    playlists['fanart'] = newfanart
                                    playlists['folder'] = folder
                                    playlists['typeXml'] = typeXml
                                    open(PlaylistFile,'a').write(str(playlists))
                                    for thumb,name,url,fanart,folder,typeXml in playlist:
                                        try:
                                        
                                            playlists['title'] = name
                                            playlists['url'] = url
                                            playlists['thumb'] = thumb
                                            playlists['fanart'] = fanart
                                            playlists['folder'] = folder
                                            playlists['typeXml'] = typeXml
                                            open(PlaylistFile,'a').write(str(playlists))
                                            xbmc.executebuiltin("XBMC.Notification([B][COLOR=FF67cc33]MashUp[/COLOR][/B],[B]Playlist Thumbnail Changed[/B],4000,"")")
                                        except: pass
                                    xbmc.executebuiltin("Container.Refresh")

def addFolder(folder):
        keyboard = xbmc.Keyboard('','[B][COLOR=FF67cc33]Enter Folder Name[/COLOR][/B]')
        keyboard.doModal()
        if (keyboard.isConfirmed() == False):
            return
        else:
            name = keyboard.getText()
            if name != '':
                if selfAddon.getSetting("folderthumb") == "true":
                    thumb = xbmcgui.Dialog().browse(2, "[B][COLOR=FF67cc33]Thumbnail File Location[/COLOR][/B]", browseType)
                else:
                    thumb= ''
                if selfAddon.getSetting("folderfanart") == "true":
                    fanart = xbmcgui.Dialog().browse(2, "[B][COLOR=FF67cc33]Fanart File Location[/COLOR][/B]", browseType)
                else:
                    fanart=''
                folders = {}
                folders['title'] = urllib.quote_plus(name)
                folders['thumb'] = urllib.quote_plus(thumb)
                folders['fanart'] = urllib.quote_plus(fanart)
                folders['folder'] = urllib.quote_plus(folder)
                if not os.path.exists(FolderFile):
                    open(FolderFile,'w').write(str(folders))
                    xbmc.executebuiltin("XBMC.Notification([B][COLOR=FF67cc33]"+name+"[/COLOR][/B],[B]Folder Created.[/B],3000,"")")
                else:
                    open(FolderFile,'a').write(str(folders))
                    xbmc.executebuiltin("XBMC.Notification([B][COLOR=FF67cc33]"+name+"[/COLOR][/B],[B]Folder Created.[/B],3000,"")")
                xbmc.executebuiltin("Container.Refresh")
            else:
                xbmc.executebuiltin("XBMC.Notification([B][COLOR=FF67cc33]Sorry![/COLOR][/B],[B]Invalid entry[/B],3000,"")")
            return
        
def openFolder(name,folders):
    if selfAddon.getSetting("addmethod") == "false":
        main.addPlayc('Add Playlist',folders,250,art+'/xmlplaylistadd.png','','','','','')
    pl=0
    fl=0
    if os.path.exists(PlaylistFile):
        playlist=re.compile("{'thumb': '(.*?)', 'title': '(.*?)', 'url': '(.*?)', 'fanart': '(.*?)', 'folder': '(.*?)', 'typeXml': '(.*?)'}").findall(open(PlaylistFile,'r').read())
        for thumb,name,url,fanart,folder,typeXml in sorted(playlist):
            if urllib.unquote_plus(folders)==urllib.unquote_plus(folder):
                name=urllib.unquote_plus(name)
                url=urllib.unquote_plus(url)
                thumb=urllib.unquote_plus(thumb)
                fanart=urllib.unquote_plus(fanart)
                if typeXml =='MashUp':
                    main.addDirXml(name,url,239,thumb,folders,fanart,'','','')
                else:
                    main.addDirXml(name,url,257,thumb,folders,fanart,typeXml,'','')
                pl=pl+1
    if os.path.exists(FolderFile):
        foldered=re.compile("{'fanart': '(.*?)', 'folder': '(.*?)', 'thumb': '(.*?)', 'title': '(.*?)'}").findall(open(FolderFile,'r').read())
        for fanart,folder,thumb,name in sorted(foldered):
            if urllib.unquote_plus(folders)==urllib.unquote_plus(folder):
                name=urllib.unquote_plus(name)
                thumb=urllib.unquote_plus(thumb)
                fanart=urllib.unquote_plus(fanart)
                main.addXmlFolder(name,folder+'-'+name,253,thumb,'',fanart,'','','')
                fl=fl+1
    if fl==0 and pl==0 and selfAddon.getSetting("addmethod") == "true":
        main.addPlayc('Add Playlist',folders,250,art+'/xmlplaylistadd.png','','','','','')
        
                
def removeFolder(title,folders):
    if os.path.exists(PlaylistFile):
        playlist=re.compile("{'thumb': '(.*?)', 'title': '(.*?)', 'url': '(.*?)', 'fanart': '(.*?)', 'folder': '(.*?)', 'typeXml': '(.*?)'}").findall(open(PlaylistFile,'r').read())
        if os.path.exists(PlaylistFile):
            for thumb,name,url,fanart,folder,typeXml in reversed (playlist):
                if urllib.unquote_plus(folders)==urllib.unquote_plus(folder):
                    playlist.remove((thumb,name,url,fanart,folder,typeXml))
                    os.remove(PlaylistFile)
                    for thumb,name,url,fanart,folder,typeXml in playlist:
                        try:
                            playlists = {}
                            playlists['title'] = name
                            playlists['url'] = url.replace('\\\\','\\')
                            playlists['thumb'] = thumb.replace('\\\\','\\')
                            playlists['fanart'] = fanart.replace('\\\\','\\')
                            playlists['folder'] = folder
                            playlists['typeXml'] = typeXml
                            open(PlaylistFile,'a').write(str(playlists))
                        except: pass
    if os.path.exists(FolderFile):
        foldered=re.compile("{'thumb': '(.*?)', 'title': '(.*?)', 'url': '(.*?)', 'fanart': '(.*?)', 'folder': '(.*?)', 'typeXml': '(.*?)'}").findall(open(FolderFile,'r').read())
        if os.path.exists(FolderFile):
            for thumb,name,url,fanart,folder,typeXml in reversed (foldered):
                if title == urllib.unquote_plus(name) and urllib.unquote_plus(folders)==urllib.unquote_plus(folder)+'-'+title:
                    foldered.remove((fanart,folder,thumb,name))
                    os.remove(FolderFile)
                    for thumb,name,url,fanart,folder,typeXml in foldered:
                        try:
                            folders = {}
                            folders['title'] = name
                            folders['thumb'] = thumb.replace('\\\\','\\')
                            folders['fanart'] = fanart.replace('\\\\','\\')
                            folders['folder'] = folder
                            open(FolderFile,'a').write(str(folders))
                            xbmc.executebuiltin("XBMC.Notification([B][COLOR=FF67cc33]"+title+"[/COLOR][/B],[B]Folder Removed from Custom Channels[/B],4000,"")")
                        except: pass

    xbmc.executebuiltin("Container.Refresh")   



def LIST(mname,murl):
    items=[]
    i=0
    if 'http' in murl:
        text = main.OPENURL(murl)
    else:
        f = open(murl)
        text = f.read()
    name=re.findall('<title>([^<]+)</title>',text)
    for names in name:
        name=re.findall('<title>([^<]+)</title>',text)
        url=re.findall('<link>([^<]+)</link>',text)
        thumb=re.findall('<thumbnail>([^<]+)</thumbnail>',text)
        if thumb:
            thumb=thumb[i]
        else:
            thumb=''
        items.append({
            'title': name[i],
            'thumbnail': thumb,
            'path': url[i]
        })
        i=i+1
    for channels in items:
        main.addPlayMs(channels['title'],channels['path'],240,channels['thumbnail'],'','','','','')

def listLS(name,url,fanart):
    ok=True
    xbmc.executebuiltin('XBMC.Container.Update (plugin://plugin.video.live.streams/?url=%s&mode=1&name=%s&fanart=%s)' % (url,name,fanart))
    return ok

    
    
def LINK(mname,murl,thumb):
        main.GA(mname,"Watched")
        ok=True
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        stream_url = main.resolve_url(murl) 
        listitem = xbmcgui.ListItem(thumbnailImage=thumb)
        listitem.setInfo('video', {'Title': mname, 'Genre': 'Custom'} )
        playlist.add(stream_url,listitem)
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(playlist)
        #WatchHistory
        if selfAddon.getSetting("whistory") == "true":
            wh.add_item(mname+' '+'[COLOR green]Custom Channel[/COLOR]', sys.argv[0]+sys.argv[2], infolabels='', img=thumb, fanart='', is_folder=False)
        return ok    

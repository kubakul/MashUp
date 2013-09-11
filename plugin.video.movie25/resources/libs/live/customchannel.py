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

def MAIN():
    folders='home'
    if selfAddon.getSetting("hideinstruction") == "false":
        main.addPlayc('My XML Channel Instructions','nills',248,art+'/xml.png','','','','','')
    if selfAddon.getSetting("addmethod") == "false":
        main.addPlayc('Add Playlist',folders,250,art+'/xml.png','','','','','')
        main.addPlayc('Add Folder',folders,252,art+'/xml.png','','','','','')
    if os.path.exists(PlaylistFile):
        playlist=re.compile("{'url': '(.*?)', 'fanart': '(.*?)', 'folder': '(.*?)', 'thumb': '(.*?)', 'title': '(.*?)'}").findall(open(PlaylistFile,'r').read())
        for url,fanart,folder,thumb,name in playlist:
            if folders==folder:
                main.addDirXml(name,url,239,thumb,folders,fanart,'','','')
    if os.path.exists(FolderFile):
        folder=re.compile("{'fanart': '(.*?)', 'folder': '(.*?)', 'thumb': '(.*?)', 'title': '(.*?)'}").findall(open(FolderFile,'r').read())
        for fanart,folder,thumb,name in folder:
            if folders==folder:
                main.addXmlFolder(name,folder+'-'+name,253,thumb,'',fanart,'','','')
    

def XmlIns():
        dir = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.movie25/resources/message', ''))
        chlg = os.path.join(dir, 'xmlchannels.txt')
        main.TextBoxes("[B][COLOR red]MashUp XML Instructions![/B][/COLOR]",chlg)

def addPlaylist(folder):
    dialog = xbmcgui.Dialog()
    ret = dialog.select('[COLOR=FF67cc33][B]Choose Entry Type[/COLOR][/B]',['[B][COLOR=FF67cc33]Browse for XML Using Filemanager[/COLOR][/B]','[B][COLOR=FF67cc33]Browse for XML Using Set User Source[/COLOR][/B]','[B][COLOR=FF67cc33]Enter XML URL[/COLOR][/B]'])
    if ret == -1:
        return
    else:
        if ret == 0:
            xmlfile = xbmcgui.Dialog().browse(1, "[B][COLOR=FF67cc33]XML File Location[/COLOR][/B]", 'programs')                        
        if ret == 1:
            xmlfile = xbmcgui.Dialog().browse(1, "[B][COLOR=FF67cc33]XML File Location[/COLOR][/B]", 'files')
        
        if ret == 2:
            keyboard = xbmc.Keyboard('','[B][COLOR=FF67cc33]Enter XML URL[/COLOR][/B]')
            keyboard.doModal()
            if (keyboard.isConfirmed() == False):
                return
            xmlfile = keyboard.getText()
        if xmlfile:
            keyboard = xbmc.Keyboard('','[B][COLOR=FF67cc33]Enter Playlist Name[/COLOR][/B]')
            keyboard.doModal()
            if (keyboard.isConfirmed() == False):
                return
            else:
                name = keyboard.getText()
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
                playlists['title'] = name
                playlists['url'] = xmlfile
                playlists['thumb'] = thumb
                playlists['fanart'] = fanart
                playlists['folder'] = folder
                if not os.path.exists(PlaylistFile):
                    open(PlaylistFile,'w').write(str(playlists))
                    xbmc.executebuiltin("XBMC.Notification([B][COLOR=FF67cc33]"+name+"[/COLOR][/B],[B]Playlist Created.[/B],3000,"")")
                else:
                    open(PlaylistFile,'a').write(str(playlists))
                    xbmc.executebuiltin("XBMC.Notification([B][COLOR=FF67cc33]"+name+"[/COLOR][/B],[B]Playlist Created.[/B],3000,"")")
                xbmc.executebuiltin("Container.Refresh")
        return

def removePlaylist(title,murl,folders):
    if os.path.exists(PlaylistFile):
        playlist=re.compile("{'url': '(.*?)', 'fanart': '(.*?)', 'folder': '(.*?)', 'thumb': '(.*?)', 'title': '(.*?)'}").findall(open(PlaylistFile,'r').read())
        if len(playlist)<=1 and str(playlist).find(title):
            os.remove(PlaylistFile)
            xbmc.executebuiltin("Container.Refresh")
        if os.path.exists(PlaylistFile):
            for url,fanart,folder,thumb,name in reversed (playlist):
                if title == name and folders==folder:
                    playlist.remove((url,fanart,folder,thumb,name))
                    os.remove(PlaylistFile)
                    for url,fanart,folder,thumb,name in playlist:
                        try:
                            playlists = {}
                            playlists['title'] = name
                            playlists['url'] = url.replace('\\\\','\\')
                            playlists['thumb'] = thumb
                            playlists['fanart'] = fanart
                            playlists['folder'] = folder
                            open(PlaylistFile,'a').write(str(playlists))
                            xbmc.executebuiltin("Container.Refresh")
                            xbmc.executebuiltin("XBMC.Notification([B][COLOR=FF67cc33]"+title+"[/COLOR][/B],[B]Playlist Removed from Custom Channels[/B],4000,"")")
                        except: pass
        else: xbmc.executebuiltin("XBMC.Notification([B][COLOR green]Mash Up[/COLOR][/B],[B]You Have No Playlists[/B],1000,"")")
    return

def addFolder(folder):
        keyboard = xbmc.Keyboard('','[B][COLOR=FF67cc33]Enter Folder Name[/COLOR][/B]')
        keyboard.doModal()
        if (keyboard.isConfirmed() == False):
            return
        else:
            name = keyboard.getText()
            if name != '':
                if selfAddon.getSetting("folderthumb") == "true":
                    thumb = xbmcgui.Dialog().browse(2, "[B][COLOR=FF67cc33]Thumbnail File Location[/COLOR][/B]", 'programs')
                else:
                    thumb= ''
                if selfAddon.getSetting("folderfanart") == "true":
                    fanart = xbmcgui.Dialog().browse(2, "[B][COLOR=FF67cc33]Fanart File Location[/COLOR][/B]", 'programs')
                else:
                    fanart=''
                folders = {}
                folders['title'] = name
                folders['thumb'] = thumb.replace('\\\\','\\')
                folders['fanart'] = fanart.replace('\\\\','\\')
                folders['folder'] = folder
                if not os.path.exists(FolderFile):
                    open(FolderFile,'w').write(str(folders))
                    xbmc.executebuiltin("XBMC.Notification([B][COLOR=FF67cc33]"+name+"[/COLOR][/B],[B]Folder Created.[/B],3000,"")")
                else:
                    open(FolderFile,'a').write(str(folders))
                    xbmc.executebuiltin("XBMC.Notification([B][COLOR=FF67cc33]"+name+"[/COLOR][/B],[B]Folder Created.[/B],3000,"")")
                xbmc.executebuiltin("Container.Refresh")
            return
        
def openFolder(name,folders):
    if selfAddon.getSetting("addmethod") == "false":
        main.addPlayc('Add Playlist',folders,250,art+'/xml.png','','','','','')
        main.addPlayc('Add Folder',folders,252,art+'/xml.png','','','','','')
    if os.path.exists(PlaylistFile):
        playlist=re.compile("{'url': '(.*?)', 'fanart': '(.*?)', 'folder': '(.*?)', 'thumb': '(.*?)', 'title': '(.*?)'}").findall(open(PlaylistFile,'r').read())
        for url,fanart,folder,thumb,name in playlist:
            if folders==folder:
                main.addDirXml(name,url,239,thumb,folders,fanart,'','','')
    if os.path.exists(FolderFile):
        folder=re.compile("{'fanart': '(.*?)', 'folder': '(.*?)', 'thumb': '(.*?)', 'title': '(.*?)'}").findall(open(FolderFile,'r').read())
        for fanart,folder,thumb,name in folder:
            if folders==folder:
                main.addXmlFolder(name,folder+'-'+name,253,thumb,'',fanart,'','','')
                
def removeFolder(title,folders):
    if os.path.exists(PlaylistFile):
        playlist=re.compile("{'url': '(.*?)', 'fanart': '(.*?)', 'folder': '(.*?)', 'thumb': '(.*?)', 'title': '(.*?)'}").findall(open(PlaylistFile,'r').read())
        if os.path.exists(PlaylistFile):
            for url,fanart,folder,thumb,name in reversed (playlist):
                if folders==folder:
                    playlist.remove((url,fanart,folder,thumb,name))
                    os.remove(PlaylistFile)
                    for url,fanart,folder,thumb,name in playlist:
                        try:
                            playlists = {}
                            playlists['title'] = name
                            playlists['url'] = url.replace('\\\\','\\')
                            playlists['thumb'] = thumb.replace('\\\\','\\')
                            playlists['fanart'] = fanart.replace('\\\\','\\')
                            playlists['folder'] = folder
                            open(PlaylistFile,'a').write(str(playlists))
                        except: pass
    if os.path.exists(FolderFile):
        foldered=re.compile("{'fanart': '(.*?)', 'folder': '(.+?)', 'thumb': '(.*?)', 'title': '(.+?)'}").findall(open(FolderFile,'r').read())
        if os.path.exists(FolderFile):
            for fanart,folder,thumb,name in reversed (foldered):
                if title == name and folders==folder+'-'+title:
                    foldered.remove((fanart,folder,thumb,name))
                    os.remove(FolderFile)
                    for fanart,folder,thumb,name in foldered:
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

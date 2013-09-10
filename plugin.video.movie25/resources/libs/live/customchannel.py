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

def MAIN():
    main.addPlayc('My XML Channel Instructions','nills',248,art+'/xml.png','','','','','')
    main.addPlayc('Add Playlist','nills',250,art+'/xml.png','','','','','')
    if os.path.exists(PlaylistFile):
        playlist=re.compile("{'url': '(.*?)', 'fanart': '(.*?)', 'thumb': '(.*?)', 'title': '(.*?)'}").findall(open(PlaylistFile,'r').read())
        for url,fanart,thumb,name in playlist:
            main.addDirMs(name,url,239,thumb,'',fanart,'','','')
    

def XmlIns():
        dir = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.movie25/resources/message', ''))
        chlg = os.path.join(dir, 'xmlchannels.txt')
        main.TextBoxes("[B][COLOR red]MashUp XML Instructions![/B][/COLOR]",chlg)

def addPlaylist():
    dialog = xbmcgui.Dialog()
    ret = dialog.select('[COLOR=FF67cc33][B]Choose Entry Type[/COLOR][/B]',['[B][COLOR=FF67cc33]Browse for XML file[/COLOR][/B]','[B][COLOR=FF67cc33]Enter XML URL[/COLOR][/B]'])
    if ret == -1:
        return
    else:
        if ret == 0:
            xmlfile = xbmcgui.Dialog().browse(1, "[B][COLOR=FF67cc33]XML File Location[/COLOR][/B]", 'files')
        
        if ret == 1:
            keyboard = xbmc.Keyboard('','[B][COLOR=FF67cc33]Enter XML URL[/COLOR][/B]')
            keyboard.doModal()
            if (keyboard.isConfirmed() == False):
                return
            xmlfile = keyboard.getText()
        keyboard = xbmc.Keyboard('','[B][COLOR=FF67cc33]Enter Playlist Name[/COLOR][/B]')
        keyboard.doModal()
        if (keyboard.isConfirmed() == False):
            return
        name = keyboard.getText()
        thumb = xbmcgui.Dialog().browse(1, "[B][COLOR=FF67cc33]Thumbnail File Location[/COLOR][/B]", 'files')
        fanart = xbmcgui.Dialog().browse(1, "[B][COLOR=FF67cc33]Fanart File Location[/COLOR][/B]", 'files')
        playlists = {}
        playlists['title'] = name
        playlists['url'] = xmlfile
        playlists['thumb'] = thumb
        playlists['fanart'] = fanart
        if not os.path.exists(PlaylistFile):
            open(PlaylistFile,'w').write(str(playlists))
            xbmc.executebuiltin("XBMC.Notification([B][COLOR=FF67cc33]"+name+"[/COLOR][/B],[B]Favourites file Created.[/B],3000,"")")
        else:
            open(PlaylistFile,'a').write(str(playlists))
            xbmc.executebuiltin("XBMC.Notification([B][COLOR=FF67cc33]"+name+"[/COLOR][/B],[B]Favourites file Created.[/B],3000,"")")

        
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
        main.addPlayL(channels['title'],channels['path'],240,channels['thumbnail'],'','','','','')
    
def LINK(mname,murl,thumb):
        main.GA(mname,"Watched")
        ok=True
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        stream_url = murl
        listitem = xbmcgui.ListItem(thumbnailImage=thumb)
        listitem.setInfo('video', {'Title': mname, 'Genre': 'Custom'} )
        playlist.add(stream_url,listitem)
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(playlist)
        #WatchHistory
        if selfAddon.getSetting("whistory") == "true":
            wh.add_item(mname+' '+'[COLOR green]Custom Channel[/COLOR]', sys.argv[0]+sys.argv[2], infolabels='', img=thumb, fanart='', is_folder=False)
        return ok    

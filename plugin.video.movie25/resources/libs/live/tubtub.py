import urllib,urllib2,re,cookielib,os,sys
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

def TubTubMAIN(murl):
        main.GA("TubTub","List")
        main.addLink('[COLOR red]Classics, Very Old Content[/COLOR]','','')
        thumb=art+'/tubtub.png'
        link=main.OPENURL(murl)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile("""<a href="mms://(.+?)"  .+?>([^<]+)</span></a>""").findall(link)
        for url,name in match:
            main.addPlayL(name,'http://'+url,186,thumb,'','','','','')
            

        
        
def TubTubLink(mname,murl):
        main.GA("TubTub-"+mname,"Watched")
        ok=True
        link=main.OPENURL(murl)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile("Ref2=([^<]+)").findall(link)
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        stream_url = match[0]
        listitem = xbmcgui.ListItem(mname)
        
        playlist.add(stream_url,listitem)
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(playlist)
        #WatchHistory
        if selfAddon.getSetting("whistory") == "true":
            wh.add_item(mname+' '+'[COLOR green]TubTub[/COLOR]', sys.argv[0]+sys.argv[2], infolabels='', img='', fanart='', is_folder=False)
        return ok

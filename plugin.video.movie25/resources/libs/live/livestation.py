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

def LivestationList(murl):
        main.GA("Live","Livestation")
        link=main.OPENURL('https://github.com/mash2k3/MashUpStreams/raw/master/livestation.xml')
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile('<title>([^<]+)</title.+?link>([^<]+)</link.+?thumbnail>([^<]+)</thumbnail>').findall(link)
        for name,url,thumb in sorted(match):
            main.addPlayL(name,url,118,thumb,'','','','','')
                       
                       


def LivestationLink(mname,murl,thumb):
        link=main.OPENURL(murl)
        link=link.replace('href="/en/sessions/new','').replace('href="/en/contacts/new">','').replace('href="/redirect?locale=en">','')
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match= re.compile('<li><a href="(.+?)">(.+?)</a></li>').findall(link)
        if len(match)>1:
            for url, name in match:
                main.addPlayL(mname+' '+name,'http://mobile.livestation.com'+url,118,thumb,'','','','','')
        else:
            LivestationLink2(mname,murl,thumb)
            
def LivestationLink2(mname,murl,thumb):
        main.GA("Livestation-"+mname,"Watched")
        ok=True
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Playing Link,1000)")
        r = re.findall('m3u8',murl)
        if r:
                stream_url =murl
                listitem = xbmcgui.ListItem(thumbnailImage=thumb)
                listitem.setInfo('video', {'Title': mname, 'Genre': 'Live'} )
                
                playlist.add(stream_url,listitem)
                xbmcPlayer = xbmc.Player()
                xbmcPlayer.play(playlist)
                #WatchHistory
                if selfAddon.getSetting("whistory") == "true":
                    wh.add_item(mname+' '+'[COLOR green]Livestation[/COLOR]', sys.argv[0]+sys.argv[2], infolabels='', img=thumb, fanart='', is_folder=False)
                return ok
        else:
        
                link=main.OPENURL(murl)
                rtmp= re.compile('"streamer":"(.+?)"').findall(link)
                match= re.compile('"file":".+?".+?"file":"([^<]+)high.sdp"').findall(link)
                if len(match)>0 and len(rtmp)>0:
                    for fid in match[0:1]:
                        stream_url = rtmp[0]+' playpath='+fid+'high.sdp swfUrl=http://beta.cdn.livestation.com/player/5.10/livestation-player.swf pageUrl='+murl
                else:
                    match3= re.compile('<source src="(.+?)" type="video/mp4"/>').findall(link)
                    if len(match3)>0:
                        for vid in match3:
                            match2= re.compile('akamedia').findall(vid)
                            if len(match2)>0:
                                stream_url =vid
                            else:
                                stream_url =vid
                    else:
                        fid= re.compile('"file":"(.+?).sdp"').findall(link)
                        stream_url = rtmp[0]+' playpath='+fid[0]+'.sdp swfUrl=http://beta.cdn.livestation.com/player/5.10/livestation-player.swf pageUrl='+murl      
                listitem = xbmcgui.ListItem(thumbnailImage=thumb)
                listitem.setInfo('video', {'Title': mname, 'Genre': 'Live'} )
                
                playlist.add(stream_url,listitem)
                xbmcPlayer = xbmc.Player()
                xbmcPlayer.play(playlist)
                #WatchHistory
                if selfAddon.getSetting("whistory") == "true":
                    wh.add_item(mname+' '+'[COLOR green]Livestation[/COLOR]', sys.argv[0]+sys.argv[2], infolabels='', img=thumb, fanart='', is_folder=False)
                return ok

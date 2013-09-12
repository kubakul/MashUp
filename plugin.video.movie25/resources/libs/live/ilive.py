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

try:
        link=main.OPENURL('https://github.com/mash2k3/MashUpNotifications/raw/master/Token.xml')
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')

except:
        link='nill'
r = re.findall(r'<token>(.+?)</token>',link)
if r:
        token=r[0]
        if token == 'DOWN':
                xbmc.executebuiltin("XBMC.Notification(Sorry!,iLive Token Needs Updating,6000)")
                
else:
        token='9898'
        

def iLive():
        main.addDir('General','general',120,art+'/ilive.png')
        main.addDir('Entertainment','entertainment',120,art+'/ilive.png')
        main.addDir('Sports','sports',120,art+'/ilive.png')
        main.addDir('News','news',120,art+'/ilive.png')
        main.addDir('Music','music',120,art+'/ilive.png')
        main.addDir('Animation','animation',120,art+'/ilive.png')
        main.GA("Live","iLive")
        
def iLiveList(murl):
        if murl=='general':
            try:
                urllist=['http://www.ilive.to/channels/General','http://www.ilive.to/channels/General?p=2']
            except:
                urllist=['http://www.ilive.to/channels/General']
        if murl=='entertainment':
            try:
                urllist=['http://www.ilive.to/channels/Entertainment','http://www.ilive.to/channels/Entertainment?p=2','http://www.ilive.to/channels/Entertainment?p=3','http://www.ilive.to/channels/Entertainment?p=4','http://www.ilive.to/channels/Entertainment?p=5','http://www.ilive.to/channels/Entertainment?p=6']
            except:
                urllist=['http://www.ilive.to/channels/Entertainment','http://www.ilive.to/channels/Entertainment?p=2','http://www.ilive.to/channels/Entertainment?p=3','http://www.ilive.to/channels/Entertainment?p=4','http://www.ilive.to/channels/Entertainment?p=5']
        if murl=='sports':
            try:
                urllist=['http://www.ilive.to/channels/Sport','http://www.ilive.to/channels/Sport?p=2','http://www.ilive.to/channels/Sport?p=3','http://www.ilive.to/channels/Sport?p=4']
            except:
                urllist=['http://www.ilive.to/channels/Sport','http://www.ilive.to/channels/Sport?p=2','http://www.ilive.to/channels/Sport?p=3']
        if murl=='news':
            try:
                urllist=['http://www.ilive.to/channels/News']
            except:
                urllist=['http://www.ilive.to/channels/News']
        if murl=='music':
            try:
                urllist=['http://www.ilive.to/channels/Music']
            except:
                urllist=['http://www.ilive.to/channels/Music']
        if murl=='animation':
            try:
                urllist=['http://www.ilive.to/channels/Animation']
            except:
                urllist=['http://www.ilive.to/channels/Animation']
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until channel list is loaded.')
        totalLinks = len(urllist)
        loadedLinks = 0
        remaining_display = 'Pages loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0,'[B]Loading.....[/B]',remaining_display)
        for durl in urllist:
                link=main.OPENURL(durl)
                link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
                match=re.compile('src=".+?" alt=".+?<img width=".+?" height=".+?" src="([^<]+)" alt=".+?"/></noscript></a><a href="(.+?)"><strong>(.+?)</strong></a><br/>').findall(link)
                for thumb,url,name in match:
                        match=re.compile('Hongkong').findall(name)
                        match2=re.compile('sex').findall(name)
                        if len(match)==0 and len(match2)==0:
                                if name != 'Playboy TV':
                                        main.addPlayL(name,url,121,thumb,'','','','','')
                
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Pages loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'[B]Loading.....[/B]',remaining_display)
                if (dialogWait.iscanceled()):
                        return False   
        dialogWait.close()
        del dialogWait
        main.GA("iLive","List") 

def iLiveLink(mname,murl,thumb):
        main.GA("iLive","Watched")
        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Opening Stream,3000)")
        link=main.OPENURL(murl)
        ok=True
        try:
                playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
                playlist.clear()
                link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
                match=re.compile('http://www.ilive.to/embed/(.+?)&width=(.+?)&height=(.+?)&autoplay=true').findall(link)
                for fid,wid,hei in match:
                    pageUrl='http://www.ilive.to/embedplayer.php?width='+wid+'&height='+hei+'&channel='+fid+'&autoplay=true'
                link=main.OPENURL(pageUrl)
                playpath=re.compile('file: "(.+?).flv"').findall(link)
                if len(playpath)==0:
                        playpath=re.compile('http://snapshots.ilive.to/snapshots/(.+?)_snapshot.jpg').findall(thumb)      
                for playPath in playpath:
                    stream_url = 'rtmp://live.iguide.to/edge playpath=' + playPath + " live=1 timeout=15 swfUrl=http://player.ilive.to/player_ilive_2.swf pageUrl="+pageUrl+" token="+token
                listitem = xbmcgui.ListItem(thumbnailImage=thumb)
                listitem.setInfo('video', {'Title': mname, 'Genre': 'Live'} )
        
                playlist.add(stream_url,listitem)
                xbmcPlayer = xbmc.Player()
                xbmcPlayer.play(playlist)
                #WatchHistory
                if selfAddon.getSetting("whistory") == "true":
                    wh.add_item(mname+' '+'[COLOR green]iLive[/COLOR]', sys.argv[0]+sys.argv[2], infolabels='', img=thumb, fanart='', is_folder=False)
                return ok
        except Exception, e:
                if stream_url != False:
                    main.ErrorReport(e)
                return ok

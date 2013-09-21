import urllib,urllib2,re,cookielib,urlresolver,os,sys
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
from resources.libs import main

#Mash Up - by Mash2k3 2012.

from t0mm0.common.addon import Addon
from universal import playbackengine, watchhistory
addon_id = 'plugin.video.movie25'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon('plugin.video.movie25', sys.argv)
art = main.art
wh = watchhistory.WatchHistory('plugin.video.movie25')

def LISTSP4(murl):
        urllist=main.OPENURL('http://oneclickmoviez.com/category/bluray/')+main.OPENURL('http://oneclickmoviez.com/category/bluray/page/2/')+main.OPENURL('http://oneclickmoviez.com/category/bluray/page/3/')+main.OPENURL('http://oneclickmoviez.com/category/bluray/page/4/')+main.OPENURL('http://oneclickmoviez.com/category/bluray/page/5/')
        if urllist:
                match=re.compile('href="(.+?)" rel="bookmark" title=".+?">(.+?)</a></h2>\n</div>\n<div class="cover">\n<div class="entry">\n\t\t\t\t\t<p style="text-align: center;"><img class="alignnone" title="poster" src="(.+?)" ').findall(urllist)
                dialogWait = xbmcgui.DialogProgress()
                ret = dialogWait.create('Please wait until Movie list is cached.')
                totalLinks = len(match)
                loadedLinks = 0
                remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(0,'[B]Will load instantly from now on[/B]',remaining_display)
                for url,name, thumb in match:
                        main.addDirM(name,url,56,thumb,'','','','','')
                        loadedLinks = loadedLinks + 1
                        percent = (loadedLinks * 100)/totalLinks
                        remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                        dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
                        if (dialogWait.iscanceled()):
                            return False    
        dialogWait.close()
        del dialogWait
        main.GA("HD","Oneclickmoviez")

def getlink(url):
        link=main.OPENURL(url)
        match=re.compile("TargetUrl = \'(.+?)\'").findall(link)
        for vlink in match:
               vid = vlink
        return vid

def LINKSP4(mname,murl):
        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Collecting Hosts,3000)")
        link=main.OPENURL(murl)
        ok=True
        link= link.replace('href="http://oneclickmoviez.com/dws/MEGA','')
        if selfAddon.getSetting("hide-download-instructions") != "true":
            main.addLink("[COLOR red]For Download Options, Bring up Context Menu Over Selected Link.[/COLOR]",'','')
        match=re.compile('<a href="(.+?)" target="_blank">(.+?)</a>.+?</p>').findall(link)
        for url, host in match:
                thumb=host.lower()
                thumb = thumb.replace('www.','').replace('.in','').replace('.net','').replace('.com','').replace('.to','').replace('.org','').replace('.ch','')
                vlink = getlink(url)
                match2=re.compile('rar').findall(vlink)
                if len(match2)==0:
                        hosted_media = urlresolver.HostedMediaFile(url=vlink, title=host)
                        match2=re.compile("{'url': '(.+?)', 'host': '(.+?)', 'media_id': '.+?'}").findall(str(hosted_media))
                        for murl,name in match2:
                                main.addDown2(mname+' [COLOR blue]'+host+'[/COLOR]',murl,211,art+'/hosts/'+thumb+".png",art+'/hosts/'+thumb+".png")

        
def LINKSP4B(mname,murl):
        main.GA("Oneclickmovies","Watched")
        ok=True
        infoLabels =main.GETMETAT(mname,'','','')
        video_type='movie'
        season=''
        episode=''
        img=infoLabels['cover_url']
        fanart =infoLabels['backdrop_url']
        imdb_id=infoLabels['imdb_id']
        infolabels = { 'supports_meta' : 'true', 'video_type':video_type, 'name':str(infoLabels['title']), 'imdb_id':str(infoLabels['imdb_id']), 'season':str(season), 'episode':str(episode), 'year':str(infoLabels['year']) }
        try:
                xbmc.executebuiltin("XBMC.Notification(Please Wait!,Resolving Link,3000)")
                stream_url = main.resolve_url(murl)
                infoL={'Title': infoLabels['title'], 'Plot': infoLabels['plot'], 'Genre': infoLabels['genre']}
                # play with bookmark
                player = playbackengine.PlayWithoutQueueSupport(resolved_url=stream_url, addon_id=addon_id, video_type=video_type, title=str(infoLabels['title']),season=str(season), episode=str(episode), year=str(infoLabels['year']),img=img,infolabels=infoL, watchedCallbackwithParams=main.WatchedCallbackwithParams,imdb_id=imdb_id)
                #WatchHistory
                if selfAddon.getSetting("whistory") == "true":
                    wh.add_item(mname+' '+'[COLOR green]OneclickMoviez[/COLOR]', sys.argv[0]+sys.argv[2], infolabels=infolabels, img=img, fanart=fanart, is_folder=False)
                player.KeepAlive()
                return ok
        except Exception, e:
                if stream_url != False:
                        main.ErrorReport(e)
                return ok

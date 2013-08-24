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


def LISTINT(name,url):
        MainUrl = "http://www.einthusan.com/movies/"
        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Collecting Source Data,5000)")
        urllist=main.OPENURL('http://www.einthusan.com/movies/index.php?lang=hindi')+main.OPENURL('http://www.einthusan.com/movies/index.php?lang=hindi&organize=Activity&filtered=RecentlyPosted&org_type=Activity&page=2')+main.OPENURL('http://www.einthusan.com/movies/index.php?lang=hindi&organize=Activity&filtered=RecentlyPosted&org_type=Activity&page=3')+main.OPENURL(
                 'http://www.einthusan.com/movies/index.php?lang=hindi&organize=Activity&filtered=RecentlyPosted&org_type=Activity&page=4')+main.OPENURL('http://www.einthusan.com/movies/index.php?lang=hindi&organize=Activity&filtered=RecentlyPosted&org_type=Activity&page=5')+main.OPENURL(
                 'http://www.einthusan.com/movies/index.php?lang=hindi&organize=Activity&filtered=RecentlyPosted&org_type=Activity&page=6')+main.OPENURL('http://www.einthusan.com/movies/index.php?lang=hindi&organize=Activity&filtered=RecentlyPosted&org_type=Activity&page=7')+main.OPENURL(
                 'http://www.einthusan.com/movies/index.php?lang=hindi&organize=Activity&filtered=RecentlyPosted&org_type=Activity&page=8')+main.OPENURL('http://www.einthusan.com/movies/index.php?lang=hindi&organize=Activity&filtered=RecentlyPosted&org_type=Activity&page=9')+main.OPENURL('http://www.einthusan.com/movies/index.php?lang=hindi&organize=Activity&filtered=RecentlyPosted&org_type=Activity&page=10')+main.OPENURL('http://www.einthusan.com/movies/index.php?lang=hindi&organize=Activity&filtered=RecentlyPosted&org_type=Activity&page=11')
        
        if urllist:
                match = re.compile('<a class="movie-cover-wrapper" href="(.+?)"><img src="(.+?)" alt="(.+?)"').findall(urllist)
                dialogWait = xbmcgui.DialogProgress()
                ret = dialogWait.create('Please wait until Movie list is cached.')
                totalLinks = len(match)
                loadedLinks = 0
                remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(0,'[B]Will load instantly from now on[/B]',remaining_display)
                for url,thumb,name in match:
                        url=url.replace('../movies/','')
                        thumb=thumb.replace('../movies/','')
                        name = name.replace('hindi movie online','')
                        main.addPlayM(name,MainUrl+url,38,MainUrl+thumb,'','','','','')
                        loadedLinks = loadedLinks + 1
                        percent = (loadedLinks * 100)/totalLinks
                        remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                        dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
                        if (dialogWait.iscanceled()):
                                return False   
        dialogWait.close()
        del dialogWait
        main.GA("INT","Einthusan")

def LINKINT(mname,url):
        main.GA("Einthusan","Watched")
        ok=True
        MainUrl = "http://www.einthusan.com/movies/"
        link=main.OPENURL(url)
        try:
                match = re.compile("'hd-2': { 'file': '(.+?)'").findall(link)
                thumb = re.compile('<img src="(../images.+?)"').findall(link)
                infoLabels =main.GETMETAT(mname,'','',thumb[0])
                video_type='movie'
                season=''
                episode=''
                img=infoLabels['cover_url']
                fanart =infoLabels['backdrop_url']
                imdb_id=infoLabels['imdb_id']
                infolabels = { 'supports_meta' : 'true', 'video_type':video_type, 'name':str(infoLabels['title']), 'imdb_id':str(infoLabels['imdb_id']), 'season':str(season), 'episode':str(episode), 'year':str(infoLabels['year']) }
                desc=' '
                for stream_url in match:
                        continue
        
                infoL={'Title': infoLabels['title'], 'Plot': infoLabels['plot'], 'Genre': infoLabels['genre']}
                # play with bookmark
                player = playbackengine.PlayWithoutQueueSupport(resolved_url=stream_url, addon_id=addon_id, video_type=video_type, title=infoLabels['title'],season=season, episode=episode, year=str(infoLabels['year']),img=img,infolabels=infoL, watchedCallbackwithParams=main.WatchedCallbackwithParams,imdb_id=imdb_id)
                #WatchHistory
                if selfAddon.getSetting("whistory") == "true":
                    wh.add_item(mname+' '+'[COLOR green]Einthusan[/COLOR]', sys.argv[0]+sys.argv[2], infolabels='', img=MainUrl+thumb[0], fanart='', is_folder=False)
                player.KeepAlive()
                return ok
        except Exception, e:
                if stream_url != False:
                    main.ErrorReport(e)
                return ok


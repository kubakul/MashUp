# -*- coding: utf-8 -*-
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


def LISTTV4(murl):
        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Collecting Source Data,10000)")
        main.addDir('Search Rlsmix','rlsmix',136,art+'/search.png')
        urllist=main.OPENURL('http://www.rlsmix.net/category/tv-shows/')+main.OPENURL('http://www.rlsmix.net/category/tv-shows/page/2/')+main.OPENURL('http://www.rlsmix.net/category/tv-shows/page/3/')+main.OPENURL('http://www.rlsmix.net/category/tv-shows/page/4/')+main.OPENURL('http://www.rlsmix.net/category/tv-shows/page/5/')+main.OPENURL('http://www.rlsmix.net/category/tv-shows/page/6/')+main.OPENURL('http://www.rlsmix.net/category/tv-shows/page/7/')+main.OPENURL('http://www.rlsmix.net/category/tv-shows/page/8/')+main.OPENURL('http://www.rlsmix.net/category/tv-shows/page/9/')+main.OPENURL('http://www.rlsmix.net/category/tv-shows/page/10/')
        
        if urllist:
                urllist=main.unescapes(urllist)
                match=re.compile('<h1 class="titles"><a href="(.+?)" title="Permanent Link to (.+?)">.+?src="http://uppix.net/(.+?)"').findall(urllist)
                dialogWait = xbmcgui.DialogProgress()
                ret = dialogWait.create('Please wait until Show list is cached.')
                totalLinks = len(match)
                loadedLinks = 0
                remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(0,'[B]Will load instantly from now on[/B]',remaining_display)
                for url,name,thumb in match:
                        match2=re.compile('TV Round Up').findall(name)
                        name=name.replace('\xc2\xa0','').replace('" ','').replace(' "','').replace('"','').replace("&#039;","'").replace("&amp;","and").replace("&#8217;","'").replace("amp;","and").replace("#8211;","-")
                        if len(match2)==0:
                            main.addDirTE(name,url,62,'http://uppix.net/'+thumb,'','','','','')
                
                        loadedLinks = loadedLinks + 1
                        percent = (loadedLinks * 100)/totalLinks
                        remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                        dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
                        if (dialogWait.iscanceled()):
                            return False   
        dialogWait.close()
        del dialogWait
        main.GA("TV","Rlsmix")

def LINKTV4(mname,url):
        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Collecting Hosts,3000)")
        link=main.OPENURL(url)
        link= link.replace('TV Rage','').replace('Homepage','').replace('href="http://www.tvrage.com','').replace('href="http://www.cbs.com','').replace('Torrent Search','').replace('Season Download','').replace('href="http://uppix.net','').replace('href="http://www.torrentz.com','').replace('href="http://directdownload.tv','')
        ok=True
        main.addLink("[COLOR red]For Download Options, Bring up Context Menu Over Selected Link.[/COLOR]",'','')
        main.addLink('[COLOR red]The Last uploaded & turbobit Link could be HD[/COLOR]','',art+'/tvb.png')
        match=re.compile('<a href="(.+?)" target="_blank">(.+?)</a>').findall(link)
        for url, host in match:
                thumb=host.lower()
                match5=re.compile('Part').findall(host)
                if len(match5)>0:
                        match6=re.compile('http://(.+?)/.+?').findall(url)
                        for url2 in match6:
                            host2 = url2.replace('www.','').replace('.in','').replace('.net','').replace('.com','').replace('.to','').replace('.org','').replace('.ch','')
                        thumb=host2.lower()
                match3=re.compile('720p').findall(url)
                match4=re.compile('mp4').findall(url)
                
                
                if len(match3)>0:
                    host =host+' [COLOR red]HD[/COLOR]'
                elif len(match4)>0:
                    host =host+' [COLOR green]SD MP4[/COLOR]'
                else:
                    host =host+' [COLOR blue]SD[/COLOR]'
                match2=re.compile('rar').findall(url)
                if len(match2)==0:
                        hosted_media = urlresolver.HostedMediaFile(url=url, title=host)
                        match2=re.compile("{'url': '(.+?)', 'host': '(.+?)', 'media_id': '.+?'}").findall(str(hosted_media))
                        for murl,name in match2:
                                main.addDown2(mname+' [COLOR blue]'+host+'[/COLOR]',murl,210,art+"/hosts/"+thumb+".png",art+"/hosts/"+thumb+".png")

        
def LINKTV4B(mname,murl):
        main.GA("RlsmixTV","Watched")
        ok=True
        infoLabels =main.GETMETAEpiT(mname,'','')
        video_type='episode'
        season=infoLabels['season']
        episode=infoLabels['episode']
        img=infoLabels['cover_url']
        fanart =infoLabels['backdrop_url']
        imdb_id=infoLabels['imdb_id']
        infolabels = { 'supports_meta' : 'true', 'video_type':video_type, 'name':str(infoLabels['title']), 'imdb_id':str(infoLabels['imdb_id']), 'season':str(season), 'episode':str(episode), 'year':str(infoLabels['year']) }
        hosted_media = urlresolver.HostedMediaFile(url=murl)
        source = hosted_media
        try:
                if source:
                        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Resolving Link,3000)")
                        stream_url = source.resolve()
                else:
                      stream_url = False
                
                infoL={'Title': infoLabels['title'], 'Plot': infoLabels['plot'], 'Genre': infoLabels['genre']}
                # play with bookmark
                player = playbackengine.PlayWithoutQueueSupport(resolved_url=stream_url, addon_id=addon_id, video_type=video_type, title=infoLabels['title'],season=str(season), episode=(episode), year=str(infoLabels['year']),img=img,infolabels=infoL, watchedCallbackwithParams=main.WatchedCallbackwithParams,imdb_id=imdb_id)
                #WatchHistory
                if selfAddon.getSetting("whistory") == "true":
                    wh.add_item(mname+' '+'[COLOR green]Rlsmix[/COLOR]', sys.argv[0]+sys.argv[2], infolabels=infolabels, img=img, fanart=fanart, is_folder=False)
                player.KeepAlive()
                return ok
        except Exception, e:
                if stream_url != False:
                        main.ErrorReport(e)
                return ok

       

def SearchhistoryRlsmix():
        seapath=os.path.join(main.datapath,'Search')
        SeaFile=os.path.join(seapath,'SearchHistoryTv')
        if not os.path.exists(SeaFile):
            url='rlsmix'
            SEARCHRlsmix(url)
        else:
            main.addDir('Search','rlsmix',137,art+'/search.png')
            main.addDir('Clear History',SeaFile,128,art+'/cleahis.png')
            thumb=art+'/link.png'
            searchis=re.compile('search="(.+?)",').findall(open(SeaFile,'r').read())
            for seahis in reversed(searchis):
                    url=seahis
                    seahis=seahis.replace('%20',' ')
                    main.addDir(seahis,url,137,thumb)
            
            
    


def SEARCHRlsmix(murl):
        seapath=os.path.join(main.datapath,'Search')
        SeaFile=os.path.join(seapath,'SearchHistoryTv')
        try:
            os.makedirs(seapath)
        except:
            pass
        if murl == 'rlsmix':
                keyb = xbmc.Keyboard('', 'Search For Shows or Movies')
                keyb.doModal()
                if (keyb.isConfirmed()):
                        search = keyb.getText()
                        encode=urllib.quote(search)
                        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Collecting Source Data,3000)")
                        urllist=main.OPENURL('http://www.rlsmix.net/?s='+encode)+main.OPENURL('http://www.rlsmix.net/page/2/?s='+encode)+main.OPENURL('http://www.rlsmix.net/page/3/?s='+encode)
                        if not os.path.exists(SeaFile) and encode != '':
                            open(SeaFile,'w').write('search="%s",'%encode)
                        else:
                            if encode != '':
                                open(SeaFile,'a').write('search="%s",'%encode)
                        searchis=re.compile('search="(.+?)",').findall(open(SeaFile,'r').read())
                        for seahis in reversed(searchis):
                            continue
                        if len(searchis)>=10:
                            searchis.remove(searchis[0])
                            os.remove(SeaFile)
                            for seahis in searchis:
                                try:
                                    open(SeaFile,'a').write('search="%s",'%seahis)
                                except:
                                    pass
        else:
                encode = murl
                
        
                try:
                        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Collecting Source Data,3000)")
                        urllist=main.OPENURL('http://www.rlsmix.net/?s='+encode)+main.OPENURL('http://www.rlsmix.net/page/2/?s='+encode)+main.OPENURL('http://www.rlsmix.net/page/3/?s='+encode)
                except:
                        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Collecting Source Data,3000)")
                        urllist=main.OPENURL('http://www.rlsmix.net/?s='+encode)+main.OPENURL('http://www.rlsmix.net/page/2/?s='+encode)
        if urllist:
                urllist=main.unescapes(urllist)
                match=re.compile('<h1 class="titles"><a href="(.+?)" title="Permanent Link to (.+?)">.+?src="http://uppix.net/(.+?)"').findall(urllist)
                dialogWait = xbmcgui.DialogProgress()
                ret = dialogWait.create('Please wait until Show list is cached.')
                totalLinks = len(match)
                loadedLinks = 0
                remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(0,'[B]Will load instantly from now on[/B]',remaining_display)
                for url,name,thumb in match:
                        match2=re.compile('TV Round Up').findall(name)
                        name=name.replace('\xc2\xa0','').replace('" ','').replace(' "','').replace('"','').replace("&#039;","'").replace("&amp;","and").replace("&#8217;","'").replace("amp;","and").replace("#8211;","-")
                        if len(match2)==0:
                                main.addDirTE(name,url,62,'http://uppix.net/'+thumb,'','','','','')
                        loadedLinks = loadedLinks + 1
                        percent = (loadedLinks * 100)/totalLinks
                        remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                        dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
                        if (dialogWait.iscanceled()):
                            return False   
        dialogWait.close()
        del dialogWait
        main.GA("Movie1k","Search")

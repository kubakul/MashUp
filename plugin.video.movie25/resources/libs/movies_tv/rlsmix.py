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


def LISTTV4(durl):
        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Collecting Source Data,1000)")
        main.addDir('Search Rlsmix','rlsmix',136,art+'/search.png')
        if 'http://directdownload.tv/' in durl:
                murl=durl
        else:
                murl='http://directdownload.tv/ajaxSearch.php?keyword=&dall&hdtv=false&pdtv=false&dsr=false&realhd=true&webdl=false&ms=false&tvshow=false&movie=false&dvdrip=false&myshows=false&offset=0'
        link=main.OPENURL(murl)
        link=main.unescapes(link)
        match=re.compile('DirectDownload.tv">(.+?)</span>(.+?)</b> </strong>.+?<dd class="links">Download<br />(.+?)</dd>').findall(link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Show list is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0,'[B]Will load instantly from now on[/B]',remaining_display)
        for name1,name2,url in match:
                name=name1+' '+name2
                name=name.replace('.',' ')
                main.addDirTE(name,url,62,'','','','','','')
                
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
                if (dialogWait.iscanceled()):
                        return False   
        dialogWait.close()
        del dialogWait   
        paginate=re.compile('http://directdownload.tv/ajaxSearch.php.?keyword=&dall&hdtv=false&pdtv=false&dsr=false&realhd=true&webdl=false&ms=false&tvshow=false&movie=false&dvdrip=false&myshows=false&offset=([^\&]+)').findall(murl)
        for page in paginate:
                i=int(page)+20
                purl='http://directdownload.tv/ajaxSearch.php?keyword=&dall&hdtv=false&pdtv=false&dsr=false&realhd=true&webdl=false&ms=false&tvshow=false&movie=false&dvdrip=false&myshows=false&offset='+str(i)
                main.addDir('[COLOR blue]Next[/COLOR]',purl,61,art+'/next2.png')
        main.GA("TV","Rlsmix")

def LINKTV4(mname,url):
        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Collecting Hosts,3000)")
        ok=True
        main.addLink("[COLOR red]For Download Options, Bring up Context Menu Over Selected Link.[/COLOR]",'','')
        match=re.compile('<a href="(.+?)" ><img title="Download on (.+?)" src=".+?">').findall(url)
        for url, host in match:
                thumb=host.lower()
                match2=re.compile('rar').findall(url)
                if len(match2)==0:
                        hosted_media = urlresolver.HostedMediaFile(url=url, title=host)
                        match2=re.compile("{'url': '(.+?)', 'host': '(.+?)', 'media_id': '.+?'}").findall(str(hosted_media))
                        for murl,name in match2:
                                main.addDown2(mname+' [COLOR blue]'+host+'[/COLOR] [COLOR red]HD[/COLOR]',murl,210,art+"/hosts/"+thumb+".png",art+"/hosts/"+thumb+".png")

        
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
                        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Collecting Source Data,1000)")
                        urllist=main.OPENURL('http://directdownload.tv/ajaxSearch.php?keyword='+encode+'&hdtv=false&pdtv=false&dsr=false&realhd=true&webdl=false&ms=false&tvshow=false&movie=false&dvdrip=false&myshows=false&offset=0')
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
                        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Collecting Source Data,1000)")
                        urllist=main.OPENURL('http://directdownload.tv/ajaxSearch.php?keyword='+encode+'&hdtv=false&pdtv=false&dsr=false&realhd=true&webdl=false&ms=false&tvshow=false&movie=false&dvdrip=false&myshows=false&offset=0')
                except:
                        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Collecting Source Data,1000)")
                        urllist=main.OPENURL('http://directdownload.tv/ajaxSearch.php?keyword='+encode+'&hdtv=false&pdtv=false&dsr=false&realhd=true&webdl=false&ms=false&tvshow=false&movie=false&dvdrip=false&myshows=false&offset=0')
        
        urllist=main.unescapes(urllist)
        match=re.compile('DirectDownload.tv">(.+?)</span>(.+?)</strong>.+?<dd class="links">Download<br />(.+?)</dd>').findall(urllist)
        #DirectDownload.tv"> The.<b>Carrie</b>.Diaries</span>.S01E01.1080p.WEB.DL.DD5.1.H.264-KiNGS </strong>1689.6 MB - 2013-01-15 12:31 (7 months ago)</dd>                    <dd class="links">Download<br />(.+?)</dd>
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Show list is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0,'[B]Will load instantly from now on[/B]',remaining_display)
        for name1,name2,url in match:
                name=name1+' '+name2
                name=name.replace('<b>.',' ').replace('</b>.',' ').replace('.<b>',' ').replace('.</b>',' ').replace('<b>',' ').replace('</b>',' ').replace('.',' ')
                main.addDirTE(name,url,62,'','','','','','')
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
                if (dialogWait.iscanceled()):
                        return False   
        dialogWait.close()
        del dialogWait
        main.GA("Movie1k","Search")

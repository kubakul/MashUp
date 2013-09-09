# -*- coding: utf-8 -*-
import urllib,urllib2,re,cookielib,urlresolver,os,sys
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
from resources.libs import main
from t0mm0.common.net import Net as net
#Mash Up - by Mash2k3 2012.

from t0mm0.common.addon import Addon
from universal import playbackengine, watchhistory
addon_id = 'plugin.video.movie25'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon('plugin.video.movie25', sys.argv)
art = main.art
smalllogo=art+'/smallicon.png'

wh = watchhistory.WatchHistory('plugin.video.movie25')

user = selfAddon.getSetting('rlsusername')
passw = selfAddon.getSetting('rlspassword')
if user == '' and passw == '':
        dialog = xbmcgui.Dialog()
        dialog.ok("[COLOR=FF67cc33]MashUp[/COLOR]", "Please set your Rlsmix credentials", "in Addon settings under logins tab.", "For credentials register @ http://directdownload.tv/.")
        selfAddon.openSettings()

def LISTTV4(durl):
        log_in = net().http_POST('http://directdownload.tv',{'username':user,'password':passw,'Login':'Login'}).content
        main.addDir('Search Rlsmix','rlsmix',136,art+'/search.png')
        if "alert('Invalid login or password.')" in log_in:
                xbmc.executebuiltin("XBMC.Notification(Sorry!,Username or Password Incorrect,10000,"+smalllogo+")")
        else:
                if 'http://directdownload.tv/' in durl:
                        murl=durl
                else:
                        murl='http://directdownload.tv/index/search/keyword//qualities/pdtv,dsr,realhd,dvdrip,webdl,webdl1080p/from/0/search'
                link = net().http_GET(murl).content
                link=main.unescapes(link)
                match=re.compile('{"release":"(.+?)","when":.+?,"size":".+?","links":(.+?),"idtvs".+?}').findall(link)
                dialogWait = xbmcgui.DialogProgress()
                ret = dialogWait.create('Please wait until Show list is cached.')
                totalLinks = len(match)
                loadedLinks = 0
                remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(0,'[B]Will load instantly from now on[/B]',remaining_display)
                for name,url in match:
                        name=name.replace('.',' ')
                        url=url.replace('\/','/')
                        main.addDirTE(name,url,62,'','','','','','')
                
                        loadedLinks = loadedLinks + 1
                        percent = (loadedLinks * 100)/totalLinks
                        remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                        dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
                        if (dialogWait.iscanceled()):
                                return False   
                dialogWait.close()
                del dialogWait   
                paginate=re.compile('http://directdownload.tv/index/search/keyword//qualities/pdtv,dsr,realhd,dvdrip,webdl,webdl1080p/from/(.+?)/search').findall(murl)
                for page in paginate:
                        i=int(page)+20
                        purl='http://directdownload.tv/index/search/keyword//qualities/pdtv,dsr,realhd,dvdrip,webdl,webdl1080p/from/'+str(i)+'/search'
                        main.addDir('[COLOR blue]Next[/COLOR]',purl,61,art+'/next2.png')
        main.GA("TV","Rlsmix")

def LINKTV4(mname,url):
        ok=True
        main.addLink("[COLOR red]For Download Options, Bring up Context Menu Over Selected Link.[/COLOR]",'','')
        match=re.compile('"(.+?)"').findall(url)
        for url in match:
                hname=re.compile("http.+?//(.+?)/.+?").findall(url)
                for host in hname:
                        host=host.replace('www.','').replace('.com','').replace('.es','').replace('.ws','').replace('.it','').replace('.net','').replace('.org','').replace('.info','')
                thumb=host.lower()
                match2=re.compile('rar').findall(url)
                if len(match2)==0:
                        hosted_media = urlresolver.HostedMediaFile(url=url, title=host)
                        match2=re.compile("{'url': '(.+?)', 'host': '(.+?)', 'media_id': '.+?'}").findall(str(hosted_media))
                        for murl,name in match2:
                                main.addDown2(mname+' [COLOR blue]'+host.upper()+'[/COLOR] [COLOR red]HD[/COLOR]',murl,210,art+"/hosts/"+thumb+".png",art+"/hosts/"+thumb+".png")

        
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
        try:
                xbmc.executebuiltin("XBMC.Notification(Please Wait!,Resolving Link,3000)")
                stream_url = main.resolve_url(murl)
                
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
        log_in = net().http_POST('http://directdownload.tv',{'username':user,'password':passw,'Login':'Login'}).content
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
                        surl='http://directdownload.tv/index/search/keyword/'+encode+'/qualities/pdtv,dsr,realhd,dvdrip,webdl,webdl1080p/from/0/search'
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
                surl='http://directdownload.tv/index/search/keyword/'+encode+'/qualities/pdtv,dsr,realhd,dvdrip,webdl,webdl1080p/from/0/search'
        link = net().http_GET(surl).content
        urllist=main.unescapes(link)
        match=re.compile('{"release":"(.+?)","when":.+?,"size":".+?","links":(.+?),"idtvs".+?}').findall(urllist)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Show list is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0,'[B]Will load instantly from now on[/B]',remaining_display)
        for name,url in match:
                name=name.replace('.',' ')
                url=url.replace('\/','/')
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


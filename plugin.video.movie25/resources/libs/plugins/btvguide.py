import urllib,urllib2,re,cookielib,string, urlparse,sys,os
import xbmc, xbmcgui, xbmcaddon, xbmcplugin,urlresolver
from t0mm0.common.net import Net as net
from resources.libs import main

#Mash Up - by Mash2k3 2012.

from t0mm0.common.addon import Addon
from universal import playbackengine, watchhistory
addon_id = 'plugin.video.movie25'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon('plugin.video.movie25', sys.argv)
art = main.art
    
wh = watchhistory.WatchHistory('plugin.video.movie25')

def MAINBTV():
        main.addDir('Search','s',558,art+'/search.png')
        main.addDir('A-Z','s',560,art+'/wfs/az.png')
        main.addDir('Todays Episodes','todays',555,art+'/wfs/toepi.png')
        main.addDir('Popular Shows','http://www.btvguide.com/shows',562,art+'/wfs/popshow.png')
        main.addDir('New Shows','http://www.btvguide.com/shows/list-type/new_shows',564,art+'/wfs/newshow.png')
        main.addDir('New Episodes (Starting from yesterdays)','http://www.btvguide.com/shows/list-type/new_episodes',565,art+'/wfs/newepi.png')
        main.addDir('By Genre','genre',566,art+'/wfs/bygen.png')
        main.addDir('By Decade','decade',566,art+'/wfs/bydec.png')
        main.addDir('By Network','network',566,art+'/wfs/bynet.png')
        main.GA("Plugin","BTV-Guide")
        main.VIEWSB()
        
def AtoZBTV():
    main.addDir('0-9','http://www.btvguide.com/shows/list-type/a_z',561,art+'/wfs/09.png')
    for i in string.ascii_uppercase:
            main.addDir(i,'http://www.btvguide.com/shows/sort/'+i.lower()+'/list-type/a_z',561,art+'/wfs/'+i+'.png')
    main.GA("BTV-Guide","A-Z")
    main.VIEWSB()

def DECADEBTV(murl):
        url ='http://www.btvguide.com/shows/list-type/a_z'
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        if murl=='decade':
            match=re.compile('<li class="filter"><a  href="/shows/decade/(.+?)">(.+?)<em>(.+?)</em></a></li>').findall(link)
            thumb=art+'/folder.png'
            for url, name, length in match:
                main.addDir(name+' '+length,'http://www.btvguide.com/shows/decade/'+url,561,thumb)
        elif murl=='genre':
            match=re.compile('<li class="filter"><a  href="/shows/category/(.+?)">(.+?)<em>(.+?)</em></a></li>').findall(link)
            thumb=art+'/folder.png'
            for url, name, length in match:
                if name!='Adult/Porn':
                    main.addDir(name+' '+length,'http://www.btvguide.com/shows/category/'+url,561,thumb)
        elif murl=='network':
            match=re.compile('<li class="filter"><a  href="/shows/network/(.+?)">(.+?)<em>(.+?)</em></a></li>').findall(link)
            thumb=art+'/folder.png'
            for url, name, length in match:
                main.addDir(name+' '+length,'http://www.btvguide.com/shows/network/'+url,561,thumb)

def SearchhistoryBTV():
        seapath=os.path.join(main.datapath,'Search')
        SeaFile=os.path.join(seapath,'SearchHistoryTv')
        if not os.path.exists(SeaFile):
            url='btv'
            SEARCHBTV(url)
        else:
            main.addDir('Search','btv',557,art+'/search.png')
            main.addDir('Clear History',SeaFile,128,art+'/cleahis.png')
            thumb=art+'/link.png'
            searchis=re.compile('search="(.+?)",').findall(open(SeaFile,'r').read())
            for seahis in reversed(searchis):
                    url=seahis
                    seahis=seahis.replace('%20',' ')
                    main.addDir(seahis,url,557,thumb)
            
            
        
def SEARCHBTV(murl):
        seapath=os.path.join(main.datapath,'Search')
        SeaFile=os.path.join(seapath,'SearchHistoryTv')
        try:
            os.makedirs(seapath)
        except:
            pass
        if murl == 'btv':
            keyb = xbmc.Keyboard('', 'Search Tv Shows')
            keyb.doModal()
            if (keyb.isConfirmed()):
                    search = keyb.getText()
                    encode=urllib.quote(search)
                    surl='http://www.btvguide.com/searchresults/?q='+encode
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
                surl='http://www.btvguide.com/searchresults/?q='+encode
        link=main.OPENURL(surl)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile('<a class="_image_container" href="(.+?)"><img class="lazy" data-original="(.+?)"src=".+?"alt="(.+?)".+?/></a>').findall(link)
        for url,thumb,name in match:
                main.addDirT(name,url,553,thumb,'','','','','')
        main.GA("BTV-Guide","Search")

            
def AllShowsBTV(murl):
        link=main.OPENURL(murl)
        link=link.replace('\r','').replace('\n','').replace('\t','')
        match=re.compile('<li class="show"><a href="(.+?)">(.+?)</a></li>').findall(link)
        for url, name in match:
            main.addDirT(name,url,553,'','','','','','')
        paginate = re.compile('<a href="([^<]+)">&gt;</a>').findall(link)
        if len(paginate)>0:
            main.addDir('Next','http://www.btvguide.com'+paginate[0],561,art+'/next2.png')
            
            

def LISTPopBTV(murl):
    if murl=='todays':
        url='http://www.btvguide.com/shows'
        link=main.OPENURL(url)
        match=re.compile('<a href="(.+?)" class=".+?" style=".+?">\r\n\t\t\t\t\t\t\t\t\t<span class=".+?">(.+?)</span>\r\n\t\t\t\t\t\t\t\t\t<span class=".+?">(.+?)\r\n\t\t\t\t\t\t\t\t\t(.+?)</span>').findall(link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Show list is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0,'[B]Will load instantly from now on[/B]',remaining_display)
        for url, name, seep, epiname in match:
            seep=seep.replace('S.','Season ').replace('E.','Episode ').replace(',','').replace(':',' ')
            main.addDirTE(name+'  '+seep+' [COLOR red]"'+epiname+'"[/COLOR]',url,559,'','','','','','')
            loadedLinks = loadedLinks + 1
            percent = (loadedLinks * 100)/totalLinks
            remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
            dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
            if (dialogWait.iscanceled()):
                return False   
        dialogWait.close()
        del dialogWait

def LISTNEWEpiBTV(murl):
        link=main.OPENURL(murl)
        link=link.replace('\r','').replace('\n','').replace('\t','')
        match=re.compile('target=".+?"><img.+?="h(.+?)" .+?/></a></div></div><div class=".+?"><h4><a href="([^<]+)" title="([^<]+)" style=".+?"  target=".+?">([^<]+)</a><div class=".+?" style=".+?">.+?</div></h4><div class=".+?" ><span class=\'_more_less\' style=".+?"><span style=".+?">([^<]+)</span>').findall(link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Show list is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0,'[B]Will load instantly from now on[/B]',remaining_display)
        for thumb, url, epiname, name, seep in match:
            seep=seep.replace(',','')
            main.addDirTE(name+' '+seep+' [COLOR red]"'+epiname+'"[/COLOR]',url,559,'h'+thumb,'','','','','')
            loadedLinks = loadedLinks + 1
            percent = (loadedLinks * 100)/totalLinks
            remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
            dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
            if (dialogWait.iscanceled()):
                return False   
        dialogWait.close()
        del dialogWait
        paginate = re.compile('<a href="([^<]+)">&gt;</a>').findall(link)
        if len(paginate)>0:
            main.addDir('Next','http://www.btvguide.com'+paginate[0],565,art+'/next2.png')

def LISTPOPShowsBTV(murl):
        desclist=[]
        i=0
        link=main.OPENURL(murl)
        link=link.replace('\r','').replace('\n','').replace('\t','')
        descr=re.compile('<span class=\'_more_less\'>([^<]+)').findall(link)
        if len(descr)>0:
            for desc in descr:
                desclist.append(desc)
        match=re.compile('<a href="([^<]+)" title="([^<]+)"><img src="([^<]+)" alt=".+?" title=".+?" width=".+?" height=".+?" />').findall(link)
        for url, name, thumb in match:
            main.addDirT(name,url,553,thumb,desclist[i],'','','','')
            i=i+1
        paginate = re.compile('<a href="([^<]+)">&gt;</a>').findall(link)
        if len(paginate)>0:
            main.addDir('Next','http://www.btvguide.com'+paginate[0],562,art+'/next2.png')

def LISTNEWShowsBTV(murl):
        desclist=[]
        i=0
        link=main.OPENURL(murl)
        link=link.replace('\r','').replace('\n','').replace('\t','')
        descr=re.compile('<span class=\'_more_less\'>([^<]+)').findall(link)
        if len(descr)>0:
            for desc in descr:
                desclist.append(desc)
        match=re.compile('<a href="([^<]+)" title="([^<]+)"><img src="([^<]+)" alt=".+?" title=".+?" width=".+?" height=".+?" />').findall(link)
        for url, name, thumb in match:
            main.addDirT(name,url,553,thumb,desclist[i],'','','','')
            i=i+1
        paginate = re.compile('<a href="([^<]+)">&gt;</a>').findall(link)
        if len(paginate)>0:
            main.addDir('Next','http://www.btvguide.com'+paginate[0],564,art+'/next2.png')

def LISTSeasonBTV(mname,murl,thumb):
        if thumb== None:
            thumb=''
        durl=murl+'/episodes'
        link=main.OPENURL(durl)
        link=link.replace('\r','').replace('\n','').replace('\t','')
        match=re.compile('<a rel="nofollow" href=".+?"><strong>([^<]+)</strong>([^<]+)</a>').findall(link)
        for seaname, epilen in match:
                furl=seaname.replace(' ','+')
                main.addDir(seaname+epilen,murl+'/season-contents/'+furl,554,thumb)

def LISTEpilistBTV(mname,murl):
        link=main.OPENURL(murl)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('"src="http://static0.btvguide.com/images/nocoverbig.png','').replace('|','')
        match=re.compile('<img class=.+?="(.+?)".+?alt="(.+?) BTVGuide".+?<a class="title" href="(.+?)"').findall(link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Show list is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0,'[B]Will load instantly from now on[/B]',remaining_display)
        for thumb, name, url in match:
                name=name.replace(':',' :')
                main.addDirTE(name,url,559,thumb,'','','','','')
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Episodes loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
                if (dialogWait.iscanceled()):
                    return False   
        dialogWait.close()
        del dialogWait
        if selfAddon.getSetting('auto-view') == 'true':
                xbmc.executebuiltin("Container.SetViewMode(%s)" % selfAddon.getSetting('episodes-view'))
                
def GETLINKBTV(murl):
    print "oob2 "+murl
    html = net().http_GET(murl).content
    next_url = re.compile('action="(.+?)" target="_blank">').findall(html)[0]
    token = re.compile('name="btvguide_csrf_token" value="(.+?)"').findall(html)[0]
    second = net().http_POST(next_url,{'submit':'','btvguide_csrf_token':token}).content
    match=re.compile('<title>GorillaVid - Just watch it!</title>').findall(second)
    if len(match)>0:
        match=re.compile('<input type="hidden" name="id" value="(.+?)">\n<input type="hidden"').findall(second)
        if len(match)>0:
            url='http://gorillavid.in/'+match[0]
            return url
        else:
            xbmc.executebuiltin("XBMC.Notification(Sorry!,Link Removed,3000)")
            return ''
    match2=re.compile('<title>DaClips - Just watch it!</title>').findall(second)
    if len(match2)>0:
        match=re.compile('<input type="hidden" name="id" value="(.+?)">\n<input type="hidden"').findall(second)
        if len(match)>0:
            url='http://daclips.in/'+match[0]
            return url
        else:
            xbmc.executebuiltin("XBMC.Notification(Sorry!,Link Removed,3000)")
            return ''
    match3=re.compile('<title>MovPod - Just watch it!</title>').findall(second)
    if len(match3)>0:
        match=re.compile('<input type="hidden" name="id" value="(.+?)">\n<input type="hidden"').findall(second)
        if len(match)>0:
            url='http://movpod.in/'+match[0]
            return url
        else:
            xbmc.executebuiltin("XBMC.Notification(Sorry!,Link Removed,3000)")
            return ''
    match4=re.compile('DivxStage').findall(second)
    if len(match4)>0:
        match=re.compile('type=".+?" value="(.+?)" id=".+?"').findall(second)
        if len(match)>0:
            url=match[0]
            return url
        else:
            xbmc.executebuiltin("XBMC.Notification(Sorry!,Link Removed,3000)")
            return ''
    match5=re.compile('<title>VidX Den').findall(second)
    if len(match5)>0:
        match=re.compile('<input name="id" type="hidden" value="(.+?)">').findall(second)
        if len(match)>0:
            url='http://www.vidxden.com/'+match[0]
            return url
        else:
            xbmc.executebuiltin("XBMC.Notification(Sorry!,Link Removed,3000)")
            return ''
    match6=re.compile('<title>VidBux').findall(second)
    if len(match6)>0:
        match=re.compile('<input name="id" type="hidden" value="(.+?)">').findall(second)
        if len(match)>0:
            url='http://www.vidbux.com/'+match[0]
            return url
        else:
            xbmc.executebuiltin("XBMC.Notification(Sorry!,Link Removed,3000)")
            return ''
    match7=re.compile('http://vidbull.com').findall(second)
    if len(match7)>0:
        match=re.compile('<input type="hidden" name="id" value="(.+?)">\n<input type="hidden"').findall(second)
        if len(match)>0:
            url='http://vidbull.com/'+match[0]
            return url
        else:
            xbmc.executebuiltin("XBMC.Notification(Sorry!,Link Removed,3000)")
            return ''
    match8=re.compile('http://flashx.tv/favicon.ico').findall(second)
    if len(match8)>0:
        match=re.compile('<meta property="og:video" content=\'(.+?)\'>').findall(second)
        if len(match)>0:
            url=match[0]
            return url
        else:
            xbmc.executebuiltin("XBMC.Notification(Sorry!,Link Removed,3000)")
            return ''
    match9=re.compile('filenuke.com').findall(second)
    if len(match9)>0:
        match=re.compile('</span> <a href="(.+?)">.+?</a>').findall(second)
        if len(match)>0:
            url=match[0]
            return url
        else:
            xbmc.executebuiltin("XBMC.Notification(Sorry!,Link Removed,3000)")
            return ''
    match10=re.compile('<title>NowVideo - Just watch it now!</title>').findall(second)
    if len(match10)>0:
        match=re.compile('type="text" value="(.+?)">').findall(second)
        if len(match)>0:
            url=match[0]
            return url
        else:
            xbmc.executebuiltin("XBMC.Notification(Sorry!,Link Removed,3000)")
            return ''
    match11=re.compile('MovShare - Reliable video hosting</title>').findall(second)
    if len(match11)>0:
        match=re.compile('id="embedtext"  value="([^<]+)">').findall(second)
        if len(match)>0:
            url=match[0]
            return url
        else:
            xbmc.executebuiltin("XBMC.Notification(Sorry!,Link Removed,3000)")
            return ''


def VIDEOLINKSBTV(mname,murl):
        main.GA("BTV-GUIDE","Watched")
        murl=murl+'/watch-online'
        link=main.OPENURL(murl)
        link=link.replace('\r','').replace('\n','').replace('\t','')
        match=re.compile('<a class="clickfreehoney" rel="nofollow" href="(.+?)"style=".+?">.+?</span>on&nbsp;(.+?)<br/>').findall(link)
        for url,host in match:
                gorillavid=re.compile('gorillavid').findall(host)
                if len(gorillavid) > 0:
                    main.addPlayc(mname+' [COLOR red]'+host+'[/COLOR]',url,563,art+'/hosts/gorillavid.png','',art+'/hosts/gorillavid.png','','','')
                daclips=re.compile('daclips').findall(host)
                if len(daclips) > 0: 
                    main.addPlayc(mname+' [COLOR red]'+host+'[/COLOR]',url,563,art+'/hosts/daclips.png','',art+'/hosts/daclips.png','','','')
                movpod=re.compile('movpod').findall(host)
                if len(movpod) > 0:
                    main.addPlayc(mname+' [COLOR red]'+host+'[/COLOR]',url,563,art+'/hosts/movpod.png','',art+'/hosts/movpod.png','','','')
                divxstage=re.compile('divxstage').findall(host)
                if len(divxstage) > 0: 
                    main.addPlayc(mname+' [COLOR red]'+host+'[/COLOR]',url,563,art+'/hosts/divxstage.png','',art+'/hosts/divxstage.png','','','')
                nowvideo=re.compile('nowvideo').findall(host)
                if len(nowvideo) > 0:
                    main.addPlayc(mname+' [COLOR red]'+host+'[/COLOR]',url,563,art+'/hosts/nowvideo.png','',art+'/hosts/nowvideo.png','','','')
                movshare=re.compile('movshare').findall(host)
                if len(movshare) > 0: 
                    main.addPlayc(mname+' [COLOR red]'+host+'[/COLOR]',url,563,art+'/hosts/movshare.png','',art+'/hosts/movshare.png','','','')
                flashx=re.compile('flashx').findall(host)
                if len(flashx) > 0:
                    main.addPlayc(mname+' [COLOR red]'+host+'[/COLOR]',url,563,art+'/hosts/flashx.png','',art+'/hosts/flashx.png','','','')
                filenuke=re.compile('filenuke').findall(host)
                if len(filenuke) > 0:
                    main.addPlayc(mname+' [COLOR red]'+host+'[/COLOR]',url,563,art+'/hosts/filenuke.png','',art+'/hosts/filenuke.png','','','')              
                vidxden=re.compile('vidxden').findall(host)
                if len(vidxden) > 0:
                    main.addPlayc(mname+' [COLOR red]'+host+'[/COLOR]',url,563,art+'/hosts/vidxden.png','',art+'/hosts/vidxden.png','','','')
                vidbux=re.compile('vidbux').findall(host)
                if len(vidbux) > 0: 
                    main.addPlayc(mname+' [COLOR red]'+host+'[/COLOR]',url,563,art+'/hosts/vidbux.png','',art+'/hosts/vidbux.png','','','')

def PLAYBTV(mname,murl):
        furl=GETLINKBTV(murl)
        ok=True
        if furl=='':
                return ok
        else:
                infoLabels =main.GETMETAEpiT(mname,'','')
                video_type='episode'
                season=infoLabels['season']
                episode=infoLabels['episode']
                img=infoLabels['cover_url']
                fanart =infoLabels['backdrop_url']
                imdb_id=infoLabels['imdb_id']
                infolabels = { 'supports_meta' : 'true', 'video_type':video_type, 'name':str(infoLabels['title']), 'imdb_id':str(infoLabels['imdb_id']), 'season':str(season), 'episode':str(episode), 'year':str(infoLabels['year']) }
                media = urlresolver.HostedMediaFile(furl)
                source = media
                try:
                    if source:
                            xbmc.executebuiltin("XBMC.Notification(Please Wait!,Resolving Link,3000)")
                            stream_url = source.resolve()
                    else:
                            stream_url = False
                    

                    infoL={'Title': infoLabels['title'], 'Plot': infoLabels['plot'], 'Genre': infoLabels['genre']}
                    # play with bookmark
                    player = playbackengine.PlayWithoutQueueSupport(resolved_url=stream_url, addon_id=addon_id, video_type=video_type, title=str(infoLabels['title']),season=str(season), episode=str(episode), year=str(infoLabels['year']),img=img,infolabels=infoL, watchedCallbackwithParams=main.WatchedCallbackwithParams,imdb_id=imdb_id)
                    #WatchHistory
                    if selfAddon.getSetting("whistory") == "true":
                        wh.add_item(mname+' '+'[COLOR green]BTV[/COLOR]', sys.argv[0]+sys.argv[2], infolabels=infolabels, img=img, fanart='', is_folder=False)
                    player.KeepAlive()
                    return ok
                except Exception, e:
                        if stream_url != False:
                                main.ErrorReport(e)
                        return ok

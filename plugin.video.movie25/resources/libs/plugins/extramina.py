#-*- coding: utf-8 -*-
import urllib,urllib2,re,cookielib,string, urlparse,sys,os
import xbmc, xbmcgui, xbmcaddon, xbmcplugin,urlresolver
from resources.libs import main

#Mash Up - by Mash2k3 2012.

from t0mm0.common.addon import Addon
from universal import playbackengine, watchhistory
addon_id = 'plugin.video.movie25'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon('plugin.video.movie25', sys.argv)
art = main.art
wh = watchhistory.WatchHistory('plugin.video.movie25')

def MAINEXTRA():
        main.addDir('Search','extra',535,art+'/wfs/searchex.png')
        #main.addDir('A-Z','http://seriesgate.tv/',538,art+'/wfs/azex.png')
        main.addDir('Recent Posts','http://www.extraminamovies.in/',532,art+'/wfs/recentex.png')
        #main.addDir('Latest Releases','latest',532,art+'/wfs/latestex.png')
        main.addDir('Genre','http://www.extraminamovies.in/',533,art+'/wfs/genreex.png')
        main.GA("Plugin","Extramina")
        main.VIEWSB()
        
def LISTEXrecent(murl):     
        if murl=='latest':
            url='http://www.extraminamovies.in/'
            link=main.OPENURL(url)
            match= re.compile('custom menu-item-.+?"><a href="(.+?)">(.+?)</a></li>').findall(link)
            for url,name in match:
                main.addPlayM(name,url,536,'','','','','','')
        else:
            link=main.OPENURL(murl)
            link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\xc2\xa0','')
            match=re.compile('<a itemprop="url" href="(.+?)" rel=".+?" title="Permanent Link to (.+?)"><img itemprop="thumbnailUrl" alt=".+?" class="smallposter" src="(.+?)"></a>.+?<span itemprop="description">(.+?)</span>').findall(link)
            dialogWait = xbmcgui.DialogProgress()
            ret = dialogWait.create('Please wait until Movie list is cached.')
            totalLinks = len(match)
            loadedLinks = 0
            remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
            dialogWait.update(0,'[B]Will load instantly from now on[/B]',remaining_display)
            if len(match)==0:
                match = re.compile('<h1 class="post-title"><a href="([^<]+)" rel=".+?" title=".+?">([^<]+)</a></h1><img style=.+? src="(.+?)">(.+?)<div').findall(link)
            for url, name, thumb,desc in match:
                main.addPlayM(name,url,536,thumb,desc,'','','','')
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
                if (dialogWait.iscanceled()):
                        return False   
            dialogWait.close()
            del dialogWait
            paginate = re.compile("<a href='([^<]+)' class='nextpostslink'>»</a>").findall(link)
            if len(paginate)>0:
                main.addDir('Next',paginate[0],532,art+'/next2.png')
                
        main.GA("Extramina","Recent")

def LISTEXgenre(murl):     
        link=main.OPENURL(murl)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\xc2\xa0','')
        match=re.compile('<a itemprop="url" href="(.+?)" rel=".+?" title="Permanent Link to (.+?)"><img itemprop="thumbnailUrl" alt=".+?" class="smallposter" src="(.+?)"></a>.+?<span itemprop="description">(.+?)</span>').findall(link)
        if len(match)==0:
                match = re.compile('<h1 class="post-title"><a href="([^<]+)" rel=".+?" title=".+?">([^<]+)</a></h1><img style=.+? src="(.+?)">(.+?)<div').findall(link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Movie list is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0,'[B]Will load instantly from now on[/B]',remaining_display)
        for url, name, thumb,desc in match:
                main.addPlayM(name,url,536,thumb,desc,'','','','')
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
                if (dialogWait.iscanceled()):
                        return False   
        dialogWait.close()
        del dialogWait
        paginate = re.compile("<a href='([^<]+)' class='nextpostslink'>»</a>").findall(link)
        if len(paginate)>0:
                main.addDir('Next',paginate[0],531,art+'/next2.png')
        main.GA("Extramina","Recent")

def GENREEXTRA(murl):
        main.addDir('Action','http://www.extraminamovies.in/category/action-movies/',531,art+'/wfs/act.png')
        main.addDir('Adventure','http://www.extraminamovies.in/category/adventure-movies/',531,art+'/wfs/adv.png')
        main.addDir('Animation','http://www.extraminamovies.in/category/animation-movies/',531,art+'/wfs/ani.png')
        main.addDir('Biography','http://www.extraminamovies.in/category/biography-movies/',531,art+'/wfs/bio.png')
        main.addDir('Bollywood','http://www.extraminamovies.in/category/bollywood-movies/',531,art+'/wfs/bollyw.png')
        main.addDir('Classics','http://www.extraminamovies.in/category/classic-movies/',531,art+'/wfs/class.png')
        main.addDir('Comedy','http://www.extraminamovies.in/category/comedy-movies/',531,art+'/wfs/com.png')
        main.addDir('Crime','http://www.extraminamovies.in/category/crime-movies/',531,art+'/wfs/cri.png')
        main.addDir('Documentary','http://www.extraminamovies.in/category/documentary-movies/',531,art+'/wfs/doc.png')
        main.addDir('Drama','http://www.extraminamovies.in/category/drama-movies/',531,art+'/wfs/dra.png')
        main.addDir('Family','http://www.extraminamovies.in/category/family-movies/',531,art+'/wfs/fam.png')
        main.addDir('Fantasy','http://www.extraminamovies.in/category/fantasy-movies/',531,art+'/wfs/fan.png')
        main.addDir('Foreign','http://www.extraminamovies.in/category/foreign-movies/',531,art+'/wfs/foriegn.png')
        main.addDir('Horror','http://www.extraminamovies.in/category/horror-movies/',531,art+'/wfs/hor.png')
        main.addDir('Music','http://www.extraminamovies.in/category/music-movies/',531,art+'/wfs/mus.png')
        main.addDir('Mystery','http://www.extraminamovies.in/category/mystery-movies/',531,art+'/wfs/mys.png')
        main.addDir('Romance','http://www.extraminamovies.in/category/romance-movies/',531,art+'/wfs/rom.png')
        main.addDir('Sci-Fi','http://www.extraminamovies.in/category/scifi-movies/',531,art+'/wfs/sci.png')
        main.addDir('Sport','http://www.extraminamovies.in/category/sport-movies/',531,art+'/wfs/spo.png')
        main.addDir('Thriller','http://www.extraminamovies.in/category/thriller-movies/',531,art+'/wfs/thr.png')
        main.addDir('War','http://www.extraminamovies.in/category/war-movies/',531,art+'/wfs/war.png')
        main.addDir('Western','http://www.extraminamovies.in/category/western-movies/',531,art+'/wfs/wes.png')
        main.GA("Extramina","Genre")
        main.VIEWSB()

def AtoZEXTRA():
        main.addDir('#','http://www.extraminamovies.in/list-of-movies/?pgno=293#char_22',531,art+'/wfs/pound.png')
        main.addDir('0-9','http://www.extraminamovies.in/list-of-movies/?pgno=1#char_31',531,art+'/wfs/09.png')
        main.addDir('A','http://www.extraminamovies.in/list-of-movies/?pgno=6#char_41',531,art+'/wfs/A.png')
        main.addDir('B','http://www.extraminamovies.in/list-of-movies/?pgno=24#char_42',531,art+'/wfs/B.png')
        main.addDir('C','http://www.extraminamovies.in/list-of-movies/?pgno=44#char_43',531,art+'/wfs/C.png')
        main.addDir('D','http://www.extraminamovies.in/list-of-movies/?pgno=60#char_44',531,art+'/wfs/D.png')
        main.addDir('E','http://www.extraminamovies.in/list-of-movies/?pgno=75#char_45',531,art+'/wfs/E.png')
        main.addDir('F','http://www.extraminamovies.in/list-of-movies/?pgno=81#char_46',531,art+'/wfs/F.png')
        main.addDir('G','http://www.extraminamovies.in/list-of-movies/?pgno=92#char_47',531,art+'/wfs/G.png')
        main.addDir('H','http://www.extraminamovies.in/list-of-movies/?pgno=99#char_48',531,art+'/wfs/H.png')
        main.addDir('I','http://www.extraminamovies.in/list-of-movies/?pgno=112#char_49',531,art+'/wfs/I.png')
        main.addDir('J','http://www.extraminamovies.in/list-of-movies/?pgno=120#char_4a',531,art+'/wfs/J.png')
        main.addDir('K','http://www.extraminamovies.in/list-of-movies/?pgno=125#char_4b',531,art+'/wfs/K.png')
        main.addDir('L','http://www.extraminamovies.in/list-of-movies/?pgno=130#char_4c',531,art+'/wfs/L.png')
        main.addDir('M','http://www.extraminamovies.in/list-of-movies/?pgno=141#char_4d',531,art+'/wfs/M.png')
        main.addDir('N','http://www.extraminamovies.in/list-of-movies/?pgno=156#char_4e',531,art+'/wfs/N.png')
        main.addDir('O','http://www.extraminamovies.in/list-of-movies/?pgno=162#char_4f',531,art+'/wfs/O.png')
        main.addDir('P','http://www.extraminamovies.in/list-of-movies/?pgno=166#char_50',531,art+'/wfs/P.png')
        main.addDir('Q','http://www.extraminamovies.in/list-of-movies/?pgno=177#char_51',531,art+'/wfs/Q.png')
        main.addDir('R','http://www.extraminamovies.in/list-of-movies/?pgno=178#char_52',531,art+'/wfs/R.png')
        main.addDir('S','http://www.extraminamovies.in/list-of-movies/?pgno=188#char_53',531,art+'/wfs/S.png')
        main.addDir('T','http://www.extraminamovies.in/list-of-movies/?pgno=214#char_54',531,art+'/wfs/T.png')
        main.addDir('U','http://www.extraminamovies.in/list-of-movies/?pgno=273#char_55',531,art+'/wfs/U.png')
        main.addDir('V','http://www.extraminamovies.in/list-of-movies/?pgno=278#char_56',531,art+'/wfs/V.png')
        main.addDir('W','http://www.extraminamovies.in/list-of-movies/?pgno=279#char_57',531,art+'/wfs/W.png')
        main.addDir('X','http://www.extraminamovies.in/list-of-movies/?pgno=289#char_58',531,art+'/wfs/X.png')
        main.addDir('Y','http://www.extraminamovies.in/list-of-movies/?pgno=289#char_59',531,art+'/wfs/Y.png')
        main.addDir('Z','http://www.extraminamovies.in/list-of-movies/?pgno=291#char_5a',531,art+'/wfs/Z.png')
        main.GA("Extramina","AZ")
        main.VIEWSB()
        

def LISTEXAZ(mname,murl):
        if mname=='#':
            link=main.OPENURL(murl)
            match = re.compile('<li><a href="(.+?)"><span class="head">(.+?)</span></a></li>').findall(link)
            for url, name in match:
                if name[0]!='Z':
                    main.addPlay(name,url,536,'')
            paginate = re.compile('<a href="([^<]+)" title="Next page">').findall(link)
            if len(paginate)>0:
                main.addDir('Next',paginate[0],531,art+'/next2.png')
        elif mname=='0-9' or mname=='Next >>':
            link=main.OPENURL(murl)
            match = re.compile('<li><a href="(.+?)"><span class="head">(.+?)</span></a></li>').findall(link)
            for url, name in match:
                    main.addPlay(name,url,536,'')
            paginate = re.compile('<a href="([^<]+)" title="Next page">').findall(link)
            if len(paginate)>0:
                main.addDir('Next >>',paginate[0],531,art+'/next2.png')
        else:
            match2 = re.compile('(.+?)xoxc(.+?)xoxc').findall(murl)
            if len(match2)>0:
                for name,url in match2:
                    mname=name
                    murl=url
            link=main.OPENURL(murl)
            match = re.compile('<li><a href="(.+?)"><span class="head">(.+?)</span></a></li>').findall(link)
            for url, name in match:
                if name[0]==mname or name[0]==mname.lower():
                    main.addPlay(name,url,536,'')
            paginate = re.compile('<a href="([^<]+)" title="Next page">').findall(link)
            if len(paginate)>0 and name[0]==mname:
                main.addDir('Next',mname+'xoxc'+paginate[0]+'xoxc',531,art+'/next2.png')
        main.GA("AZ","Movie-list")
def SearchhistoryEXTRA():
        seapath=os.path.join(main.datapath,'Search')
        SeaFile=os.path.join(seapath,'SearchHistory25')
        if not os.path.exists(SeaFile):
            url='extra'
            SEARCHEXTRA(url)
        else:
            main.addDir('Search','extra',534,art+'/search.png')
            main.addDir('Clear History',SeaFile,128,art+'/cleahis.png')
            thumb=art+'/link.png'
            searchis=re.compile('search="(.+?)",').findall(open(SeaFile,'r').read())
            for seahis in reversed(searchis):
                    url=seahis
                    seahis=seahis.replace('%20',' ')
                    main.addDir(seahis,url,534,thumb)
            
            
        
def SEARCHEXTRA(murl):
        seapath=os.path.join(main.datapath,'Search')
        SeaFile=os.path.join(seapath,'SearchHistory25')
        try:
            os.makedirs(seapath)
        except:
            pass
        if murl == 'extra':
            keyb = xbmc.Keyboard('', 'Search Movies')
            keyb.doModal()
            if (keyb.isConfirmed()):
                    search = keyb.getText()
                    encode=urllib.quote(search)
                    surl='http://www.extraminamovies.in/?s='+encode
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
                surl='http://www.extraminamovies.in/?s='+encode
        link=main.OPENURL(surl)
        link=link.replace('\xc2\xa0','').replace('\n','')
        match = re.compile('<a href="([^<]+)" rel=".+?" title=".+?">(.+?)</a>').findall(link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Movie list is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0,'[B]Will load instantly from now on[/B]',remaining_display)
        for url, name in match:
            main.addPlayM(name,url,536,'','','','','','')
            loadedLinks = loadedLinks + 1
            percent = (loadedLinks * 100)/totalLinks
            remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
            dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
            if (dialogWait.iscanceled()):
                    return False   
        dialogWait.close()
        del dialogWait
        main.GA("Extramina","Search")
        
def VIDEOLINKSEXTRA(mname,murl,thumb,desc):
        main.GA("Extramina","Watched")
        sources = []
        link=main.OPENURL(murl)
        ok=True
        infoLabels =main.GETMETAT(mname,'','',thumb)
        video_type='movie'
        season=''
        episode=''
        img=infoLabels['cover_url']
        fanart =infoLabels['backdrop_url']
        imdb_id=infoLabels['imdb_id']
        infolabels = { 'supports_meta' : 'true', 'video_type':video_type, 'name':str(infoLabels['title']), 'imdb_id':str(infoLabels['imdb_id']), 'season':str(season), 'episode':str(episode), 'year':str(infoLabels['year']) }
        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Collecting hosts,5000)")
        match=re.compile('<div class="streamlink"><a target=".+?" href="(.+?)">(.+?)</a></div>').findall(link)
        for url, host in match:
                match3=re.compile('extraminamovies').findall(url)
                if len(match3)>0:
                    link2=main.OPENURL(url)
                    match = re.compile('<iframe src="(.+?)"').findall(link2)
                    if len(match)==0:
                        match = re.compile('src="(.+?)"').findall(link2)
                    for url in match:
                        match2=re.compile('http://(.+?)/.+?').findall(url)
                        for host in match2:
                            host = host.replace('www.','')
                            if host =='putlocker.com':
                                url=url.replace('embed','file')
                hosted_media = urlresolver.HostedMediaFile(url=url, title=host)
                sources.append(hosted_media)        
        if (len(sources)==0):
                xbmc.executebuiltin("XBMC.Notification(Sorry!,Show doesn't have playable links,5000)")
      
        else:
                source = urlresolver.choose_source(sources)
        try:
                if source:
                        stream_url = source.resolve()
                else:
                      stream_url = False
                      return
                infoL={'Title': infoLabels['title'], 'Plot': infoLabels['plot'], 'Genre': infoLabels['genre']}
                # play with bookmark
                player = playbackengine.PlayWithoutQueueSupport(resolved_url=stream_url, addon_id=addon_id, video_type=video_type, title=str(infoLabels['title']),season=str(season), episode=str(episode), year=str(infoLabels['year']),img=img,infolabels=infoL, watchedCallbackwithParams=main.WatchedCallbackwithParams,imdb_id=imdb_id)
                #WatchHistory
                if selfAddon.getSetting("whistory") == "true":
                    wh.add_item(mname+' '+'[COLOR green]Extramina[/COLOR]', sys.argv[0]+sys.argv[2], infolabels=infolabels, img=img, fanart='', is_folder=False)
                player.KeepAlive()
                return ok
        except Exception, e:
                if stream_url != False:
                        main.ErrorReport(e)
                return ok

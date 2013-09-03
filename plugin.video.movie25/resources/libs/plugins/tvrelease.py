import urllib, urllib2, re, string, urlparse, sys,   os
import xbmc, xbmcgui, xbmcaddon, xbmcplugin, HTMLParser
from resources.libs import main
from t0mm0.common.addon import Addon

addon_id = 'plugin.video.movie25'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon(addon_id, sys.argv)

    
art = main.art
error_logo = art+'/bigx.png'

try:
    import urllib, urllib2, re, string, urlparse, sys, os
    
    from t0mm0.common.net import Net
    from metahandler import metahandlers
    from sqlite3 import dbapi2 as database
    from universal import playbackengine, watchhistory
    import urlresolver
except Exception, e:
    addon.log_error(str(e))
    addon.show_small_popup('MashUP: Tv-Release','Failed To Import Modules', 5000, error_logo)
    addon.show_ok_dialog(['Failed To Import Modules','Please Post Logfile In MashUP Forum @','http://www.xbmchub.com'],
                          'MashUP: TV-Release')
net = Net()
BASEURL = 'http://www.tv-release.net/'
wh = watchhistory.WatchHistory(addon_id)

def MAINMENU():
    main.addDir('Search Tv-Release',    BASEURL+'?s=',                            1006,art+'/tvrsearch1.png')
    main.addDir('TV 480',               BASEURL+'category/tvshows/tv480p/',       1001,art+'/TV480.png')
    main.addDir('TV 720',               BASEURL+'category/tvshows/tv720p/',       1001,art+'/TV720.png')
    main.addDir('TV MP4',               BASEURL+'category/tvshows/tvmp4/',        1001,art+'/TVmp4.png')
    main.addDir('TV Xvid',              BASEURL+'category/tvshows/tvxvid/',       1001,art+'/TVxvid.png')
    main.addDir('TV Packs',             BASEURL+'tv-pack/',                       1007,art+'/TVpacks.png')
    main.addDir('TV Foreign',           BASEURL+'category/tvshows/tv-foreign/',   1001,art+'/TVforeign.png')
    main.addDir('Movies 480',           BASEURL+'category/movies/movies480p/',    1001,art+'/Movies480.png')
    main.addDir('Movies 720',           BASEURL+'category/movies/movies720p/',    1001,art+'/Movies720.png')
    main.addDir('Movies Xvid',          BASEURL+'category/movies/moviesxvid/',    1001,art+'/Moviesxvid.png')
    main.addDir('Movies Foreign',       BASEURL+'category/movies/moviesforeign/', 1001,art+'/Moviesforeign.png')
    main.addSpecial('Resolver Settings',BASEURL,                                  1004,art+'/tvrresolver.png')
    main.VIEWSB()

def INDEX(url):
    types = []
    SearchType = None
    if '!' in url:
        r = url.rpartition('!')
        print r
        url = r[0]
        SearchType = r[2]
    else:
        url = url
    if '/tvshows/' in url:
        types = 'tv'
    elif '/movies/' in url:
        types = 'movie'
    html = GETHTML(url)
    if html == None:
        return
    pattern = 'tag">(.+?)</a>.+?text-align:left.+?a href="(.+?)"><b><font size="\d+px">(.+?)</font>'
    r = re.findall(pattern, html, re.I|re.M|re.DOTALL)
    dialogWait = xbmcgui.DialogProgress()
    ret = dialogWait.create('Please wait until list is cached.')
    totalLinks = len(r)
    loadedLinks = 0
    remaining_display = 'Media loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
    dialogWait.update(0,'[B]Will load instantly from now on[/B]',remaining_display)
    for tag, url, name in r:
        if re.findall('\ss\d+e\d+\s', name, re.I|re.DOTALL):
            r = re.findall('(.+?)\ss(\d+)e(\d+)\s', name, re.I)
            for name, season, episode in r:
                name = name+' Season '+season+' Episode '+episode+' ('+season+'x'+episode+')'
        elif re.findall('\s\d{4}\s\d{2}\s\d{2}\s', name):
            r = re.findall('(.+?)\s(\d{4})\s(\d{2})\s(\d{2})\s',name)
            for name, year, month, day in r:
                name = name+' '+year+' '+month+' '+day
        elif re.findall('\d+p\s', name):
            r = re.findall('(.+?)\s\d+p\s', name)
            for name in r:
                pass
        elif re.findall('\shdtv\sx', name, re.I):
            r = re.findall('(.+?)\shdtv\sx',name, re.I)
            for name in r:
                pass
        name = name+' [COLOR blue]'+tag+'[/COLOR]'
        if SearchType == None:
            if 'TV' in tag:
                main.addDirTE(name,url,1003,'','','','','','')
            elif 'Movies' in tag:
                if re.findall('\s\d+\s',name):
                    r = name.rpartition('\s\d{4}\s')
                main.addDirM(name,url,1003,'','','','','','')
        elif SearchType == 'tv' and 'TV' in tag:
            main.addDirTE(name,url,1003,'','','','','','')
        elif SearchType == 'movie' and 'Movies' in tag:
            r = name.rpartition('\s\d{4}\s')
            main.addDirM(name,url,1003,'','','','','','')
        
        loadedLinks = loadedLinks + 1
        percent = (loadedLinks * 100)/totalLinks
        remaining_display = 'Media loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
        if (dialogWait.iscanceled()):
            return False
    dialogWait.close()
    del dialogWait
    if '<!-- Zamango Pagebar 1.3 -->' in html:
        r = re.findall('<span class=\'zmg_pn_current\'>(\d+)</span>\n<span class=\'zmg_pn_standar\'><a href=\'(http://tv-release.net/category/.+?/\d+)\' title=\'Page \d+ of (\d+)\'>\d+</a>',html, re.I|re.DOTALL|re.M)
        if len(r) == 0:
            r = re.findall('<span class=\'zmg_pn_current\'>(\d+)</span>\n<span class=\'zmg_pn_standar\'><a href=\'(http://tv-release.net/page/\d+\?.+?)\' title=\'Page \d+ of (\d+)\'>\d+</a>', html, re.I|re.DOTALL|re.M)
        for current, url, total in r:
            name = '[COLOR green]Page '+current+' of '+total+', Next Page >>>[/COLOR]'
            main.addDir(name, url.replace('%5C',''), 1001, art+'/nextpage.png')
            url = url+':'+total
            name = '[COLOR green]Goto Page[/COLOR]'
            main.addDir(name, url, 1002, art+'/gotopagetr.png')
    main.VIEWS()

def LISTHOSTERS(name,url):
    html = GETHTML(url)
    if html == None: return
    main.addLink("[COLOR red]For Download Options, Bring up Context Menu Over Selected Link.[/COLOR]",'','')
    r = re.findall(r'class="td_cols"><a target=\'_blank\'.+?href=\'(.+?)\'>',html, re.M|re.DOTALL)
    try:
        t = re.findall(r'rel="nofollow">((?!.*\.rar).*)</a>', html, re.I)
        r = r+t
    except:
        pass
    if len(r) == 0:
        addon.show_ok_dialog(['No Playable Streams Found,','It Might Be That They Are Still Being Uploaded,',
                              'Or They Are Unstreamable Archive Files'],'MashUP: TV-Release')
        return
    sources = []
    for url in r:
        media = urlresolver.HostedMediaFile(url=url)
        sources.append(media)
    sources = urlresolver.filter_source_list(sources)
    r = re.findall(r'\'url\': \'(.+?)\', \'host\': \'(.+?)\'', str(sources), re.M)
    for url, host in r:
        r = re.findall(r'(.+?)\.',host)
        if 'www.real-debrid.com' in host:
            host = re.findall(r'//(.+?)/', url)
            host = host[0].replace('www.','')
            host = host.rpartition('.')
            host = host[0]
        else:
            host = r[0]
        main.addDown2(name+"[COLOR blue] :"+host.upper()+"[/COLOR]",url,1005,art+'/hosts/'+host+'.png',art+'/hosts/'+host+'.png')

def SEARCHhistory():
    dialog = xbmcgui.Dialog()
    ret = dialog.select('[COLOR green][B]Choose A Search Type[/COLOR][/B]',['[B][COLOR=FF67cc33]TV Shows[/COLOR][/B]','[B][COLOR=FF67cc33]Movies[/COLOR][/B]'])
    if ret == -1:
        return MAINMENU()
    if ret == 0:
        searchType = 'tv'
        seapath=os.path.join(main.datapath,'Search')
        SeaFile=os.path.join(seapath,'SearchHistoryTv')
        if not os.path.exists(SeaFile):
            SEARCH(searchType)
        else:
            main.addDir('Search','tv',1008,art+'/search.png')
            main.addDir('Clear History',SeaFile,128,art+'/cleahis.png')
            thumb=art+'/link.png'
            searchis=re.compile('search="(.+?)",').findall(open(SeaFile,'r').read())
            for seahis in reversed(searchis):
                    url=seahis
                    seahis=seahis.replace('%20',' ')
                    url = 'http://tv-release.net/?s='+url+'&cat=163'
                    main.addDir(seahis,url,1001,thumb)
    if ret == 1:
        searchType = 'movie'
        seapath=os.path.join(main.datapath,'Search')
        SeaFile=os.path.join(seapath,'SearchHistory25')
        if not os.path.exists(SeaFile):
            SEARCH(searchType)
        else:
            main.addDir('Search','movie',1008,art+'/search.png')
            main.addDir('Clear History',SeaFile,128,art+'/cleahis.png')
            thumb=art+'/link.png'
            searchis=re.compile('search="(.+?)",').findall(open(SeaFile,'r').read())
            for seahis in reversed(searchis):
                    url=seahis
                    seahis=seahis.replace('%20',' ')
                    url = 'http://tv-release.net/?s='+url+'&cat=164'
                    main.addDir(seahis,url,1001,thumb)



def SEARCH(murl):
    if murl == 'tv':
        seapath=os.path.join(main.datapath,'Search')
        SeaFile=os.path.join(seapath,'SearchHistoryTv')
        try:
            os.makedirs(seapath)
        except:
            pass
            keyb = xbmc.Keyboard('', '[COLOR=FF67cc33]MashUP: Search For Shows or Episodes[/COLOR]')
            keyb.doModal()
            if (keyb.isConfirmed()):
                    search = keyb.getText()
                    encode=urllib.quote(search)
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
                    url = 'http://tv-release.net/?s='+encode+'&cat=163'
                    INDEX(url)
            else:
                return MAINMENU()
    elif murl=='movie':
        seapath=os.path.join(main.datapath,'Search')
        SeaFile=os.path.join(seapath,'SearchHistory25')
        try:
            os.makedirs(seapath)
        except:
            pass
            keyb = xbmc.Keyboard('', '[COLOR=FF67cc33]MashUP: Search For Movies[/COLOR]')
            keyb.doModal()
            if (keyb.isConfirmed()):
                    search = keyb.getText()
                    encode=urllib.quote(search)
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
                    url = 'http://tv-release.net/?s='+encode+'&cat=164'
                    INDEX(url)
            else:
                return MAINMENU()

        

def TVPACKS(url):
    html = GETHTML(url)
    if html == None:
        return
    pattern = '<li><a href="(.+?)"><span class="head">(.+?)</span>'
    r = re.findall(pattern,html)
    for url, name in r:
        main.addDir(name, url, 1001,'')
        
    
    
                
def GOTOP(url):
    default = url
    r = url.rpartition(':')
    url = re.findall('(.+page\/)\d+',r[0])
    url = url[0]
    total = r[2]
    keyboard = xbmcgui.Dialog().numeric(0, '[B][I]Goto Page Number[/B][/I]')
    if keyboard > total or keyboard == '0':
        addon.show_ok_dialog(['Please Do Not Enter a Page Number bigger than',''+total+', Enter A Number Between 1 and '+total+'',
                              ''], 'MashUP: TV-Release')
        GOTOP(default)
    url = url+keyboard
    INDEX(url)
        
        
def PLAYMEDIA(name,url):
    ok = True
    r = re.findall(r'(.+?)\[COLOR', name)
    name = r[0]
    r=re.findall('Season(.+?)Episode([^<]+)',name)
    if r:
        infoLabels =main.GETMETAEpiT(name,'','')
        video_type='episode'
        season=infoLabels['season']
        episode=infoLabels['episode']
    else:
        infoLabels =main.GETMETAT(name,'','','')
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
            wh.add_item(hname+' '+'[COLOR=FF67cc33]TvRelease[/COLOR]', sys.argv[0]+sys.argv[2], infolabels=infolabels, img=str(img), fanart=str(fanart), is_folder=False)
        player.KeepAlive()
        return ok
    except:
        return ok

def GETHTML(url):
    try:
        h = net.http_GET(url).content
        if '<h2>Under Maintenance</h2>' in h:
            addon.show_ok_dialog(['[COLOR=FF67cc33][B]TV-Release is Down For Maintenance,[/COLOR][/B]',
                                  '[COLOR=FF67cc33][B]Please Try Again Later[/COLOR][/B]',''],'MashUP: TV-Release')
            return MAINMENU()
        return h.encode("utf-8")
    except urllib2.URLError, e:
        addon.show_small_popup('MashUP: Tv-Release','TV-Release Web Site Failed To Respond, Check Log For Details', 9000, error_logo)
        addon.log_notice(str(e))
        return MAINMENU()
    



import urllib,urllib2,re,cookielib,sys,os,urlresolver
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
from resources.libs import main, debridroutines
from t0mm0.common.net import Net as net
from t0mm0.common.addon import Addon
from urlresolver import common

#Mash Up - by Mash2k3 2012.


from universal import playbackengine, watchhistory
addon_id = 'plugin.video.movie25'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon('plugin.video.movie25', sys.argv)
art = main.art
elogo = xbmc.translatePath('special://home/addons/plugin.video.movie25/resources/art/bigx.png')
refererTXT = xbmc.translatePath('special://home/addons/plugin.video.movie25/resources/message/referer.txt')    
wh = watchhistory.WatchHistory('plugin.video.movie25')

def Mplaylists(murl):
        link=main.OPENURL(murl)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        r=re.findall('<poster>(.+?)</poster>',link)
        if r:
                vip=r[0]
        else:
                vip='Unknown'
        f=re.findall('<fanart>(.+?)</fanart>',link)
        if f:
                fan=f[0]
        else:
                fan=art+'/fanart2.jpg'
        match=re.compile('<name>(.+?)</name><link>(.+?)</link><thumbnail>(.+?)</thumbnail><date>(.+?)</date>').findall(link)
        for name,url,thumb,date in match:
                if '</vip>' in url:
                        main.addDirc(name+' [COLOR red] '+date+'[/COLOR]',url,260,thumb,'',fan,'','','')
                else:
                        main.addDirc(name+' [COLOR red] '+date+'[/COLOR]',url,236,thumb,'',fan,'','','')
        info=re.findall('<info><message>(.+?)</message><thumbnail>(.+?)</thumbnail></info>',link)
        if info:
            for msg,pic in info:
                main.addLink(msg,'',pic)
        popup=re.compile('<popup><name>([^<]+)</name.+?popImage>([^<]+)</popImage.+?thumbnail>([^<]+)</thumbnail></popup>').findall(link)
        for name,image,thumb in popup:
                main.addPlayc(name,image,244,thumb,'',fan,'','','')
        main.GA("MoviePL",vip+"-Directory")


        

def MList(mname,murl):
        mname  = mname.split('[C')[0]
        link=main.OPENURL(murl)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        r=re.findall('<poster>(.+?)</poster>',link)
        if r:
                vip=r[0]
        else:
                vip='Unknown'
        f=re.findall('<fanart>(.+?)</fanart>',link)
        if f:
                fan=f[0]
        else:
                fan=art+'/fanart2.jpg'
        info=re.findall('<info><message>(.+?)</message><thumbnail>(.+?)</thumbnail></info>',link)
        if info:
            for msg,pic in info:
                main.addLink(msg,'',pic)
        popup=re.compile('<popup><name>([^<]+)</name.+?popImage>([^<]+)</popImage.+?thumbnail>([^<]+)</thumbnail></popup>').findall(link)
        for name,image,thumb in popup:
                main.addPlayc(name,image,244,thumb,'',fan,'','','')
                
        directory=re.compile('<dir><name>([^<]+)</name.+?link>([^<]+)</link.+?thumbnail>([^<]+)</thumbnail></dir>').findall(link)
        for name,url,thumb in directory:
                main.addDirb(name,url,236,thumb,fan)
        
        match=re.compile('<title>([^<]+)</title.+?link>(.+?)</link.+?thumbnail>([^<]+)</thumbnail>').findall(link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Movie list is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0,'[B]Will load instantly from now on[/B]',remaining_display)
        for name,url,thumb in match:
                
                if '</sublink>' in url:
                        main.addDown4(name+' [COLOR blue]'+vip+'[/COLOR]',url,249,thumb,'',fan,'','','')
                elif '</referer>' in url:
                        main.addDown4(name+' [COLOR blue]'+vip+'[/COLOR]',url,259,thumb,'',fan,'','','')
                        
                else:        
                        main.addDown4(name+' [COLOR blue]'+vip+'[/COLOR]',url,237,thumb,'',fan,'','','')
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
                if (dialogWait.iscanceled()):
                        return False   
        dialogWait.close()
        del dialogWait
        main.GA(vip+"-Directory",vip+"-Playlist")



def subLink(mname,suburl):
        match=re.compile('<sublink>(.+?)</sublink>').findall(suburl)
        for url in match:
                match6=re.compile('http://(.+?)/.+?').findall(url)
                for url2 in match6:
                        host = url2.replace('www.','').replace('.in','').replace('.net','').replace('.com','').replace('.to','').replace('.org','').replace('.ch','')
                        if re.findall('\d+.\d+.\d+.\d+',host):
                            host='Static Link'
                        main.addDown2(mname+' [COLOR blue]'+host.upper()+'[/COLOR]',url,237,art+'/hosts/'+host.lower()+'.png',art+'/hosts/'+host.lower()+'.png')

def MLink(mname,murl,thumb):
        main.GA(mname,"Watched")
        ok=True
        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Opening Link,5000)")
        infoLabels =main.GETMETAT(mname,'','','')
        video_type='movie'
        season=''
        episode=''
        img=infoLabels['cover_url']
        fanart =infoLabels['backdrop_url']
        imdb_id=infoLabels['imdb_id']
        infolabels = { 'supports_meta' : 'true', 'video_type':video_type, 'name':str(infoLabels['title']), 'imdb_id':str(infoLabels['imdb_id']), 'season':str(season), 'episode':str(episode), 'year':str(infoLabels['year']) }
        try:
            stream_url = main.resolve_url(murl)
            if stream_url == False:
                  return                                                            
            infoL={'Title': infoLabels['title'], 'Plot': infoLabels['plot'], 'Genre': infoLabels['genre'], 'originaltitle': infoLabels['metaName']}
            # play with bookmark
            stream_url=stream_url.replace(' ','%20')
            player = playbackengine.PlayWithoutQueueSupport(resolved_url=stream_url, addon_id=addon_id, video_type=video_type, title=str(infoLabels['title']),season=str(season), episode=str(episode), year=str(infoLabels['year']),img=img,infolabels=infoL, watchedCallbackwithParams=main.WatchedCallbackwithParams,imdb_id=imdb_id)
            #WatchHistory
            if selfAddon.getSetting("whistory") == "true":
                wh.add_item(mname+' '+'[COLOR green]VIPlaylist[/COLOR]', sys.argv[0]+sys.argv[2], infolabels=infolabels, img=img, fanart=fanart, is_folder=False)
            player.KeepAlive()
            return ok
        except Exception, e:
                if stream_url != False:
                        main.ErrorReport(e)
                return ok

def refererResolver(url):
        Names = []
        for line in open(refererTXT,'r').readlines():
                Names.append(line.strip())
        from random import choice
        refer=choice(Names)
        stream_url = False
        if re.search('vidto',url,re.I):
                stream_url=resolve_videto(url,refer)
                
        elif re.search('mightyupload',url,re.I):
                stream_url=resolve_mightyupload(url,refer)               
        else:
                source = urlresolver.HostedMediaFile(url)
                if source:
                    stream_url = source.resolve()
                else:
                    stream_url=url
        return stream_url

def resolve_videto(url,referer):
    user_agent='Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
    from resources.libs import jsunpack
    try:
        html = net(user_agent).http_GET(url).content
        addon.log_error('Mash Up: Resolve Vidto - Requesting GET URL: '+url)
        r = re.findall(r'<font class="err">File was removed</font>',html,re.I)
        if r:
            addon.log_error('Mash Up: Resolve Vidto - File Was Removed')
            xbmc.executebuiltin("XBMC.Notification(File Not Found,Vidto,2000)")
            return False
        if not r:
            r = re.findall(r'(eval\(function\(p,a,c,k,e,d\)\{while.+?flvplayer.+?)</script>'
                           ,html,re.M|re.DOTALL)
            if r:
                unpacked = jsunpack.unpack(r[0])#this is where it will error, not sure if resources,libs added to os path
                r = re.findall(r'label:"\d+p",file:"(.+?)"}',unpacked)
            if not r:
                r = re.findall('type="hidden" name="(.+?)" value="(.+?)">',html)
                post_data = {}
                for name, value in r:
                    post_data[name] = value
                post_data['usr_login'] = ''
                post_data['referer'] = referer
                addon.show_countdown(7, 'Please Wait', 'Resolving')
                headers={'Referer':referer}
                html = net(user_agent).http_POST(url,post_data,headers).content
                r = re.findall(r'(eval\(function\(p,a,c,k,e,d\)\{while.+?flvplayer.+?)</script>'
                               ,html,re.M|re.DOTALL)
                if r:
                    unpacked = jsunpack.unpack(r[0])
                    r = re.findall(r'label:"\d+p",file:"(.+?)"}',unpacked)
                if not r:
                    r = re.findall(r"var file_link = '(.+?)';",html)
        return r[0]
    except Exception, e:
        print 'Mash Up: Resolve Vidto Error - '+str(e)
        addon.show_small_popup('[B][COLOR green]Mash Up: Vidto Resolver[/COLOR][/B]','Error, Check XBMC.log for Details',
                               5000, elogo)

def resolve_mightyupload(url,referer):
    from resources.libs import jsunpack
    try:
        html = net().http_GET(url).content
        addon.log_error('Mash Up: Resolve MightyUpload - Requesting GET URL: '+url)
        r = re.findall(r'name="(.+?)" value="?(.+?)"', html, re.I|re.M)
        post_data = {}
        for name, value in r:
            post_data[name] = value
        post_data['referer'] = referer
        headers={'Referer':referer}
        html = net().http_POST(url, post_data).content
        r = re.findall(r'<a href=\"(.+?)(?=\">Download the file</a>)', html)
        return r[0]
    except Exception, e:
        print 'Mash Up: Resolve MightyUpload Error - '+str(e)
        addon.show_small_popup('[B][COLOR green]Mash Up: MightyUpload Resolver[/COLOR][/B]','Error, Check XBMC.log for Details',
                               5000, elogo)
        return

def MLink2(mname,murl,thumb):
        match=re.compile('<referer>(.+?)</referer>').findall(murl)
        if match:
                video=match[0]
        else:
                video=murl
                
        main.GA(mname,"Watched")
        ok=True
        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Opening Link,5000)")
        infoLabels =main.GETMETAT(mname,'','','')
        video_type='movie'
        season=''
        episode=''
        img=infoLabels['cover_url']
        fanart =infoLabels['backdrop_url']
        imdb_id=infoLabels['imdb_id']
        infolabels = { 'supports_meta' : 'true', 'video_type':video_type, 'name':str(infoLabels['title']), 'imdb_id':str(infoLabels['imdb_id']), 'season':str(season), 'episode':str(episode), 'year':str(infoLabels['year']) }
        try:
            stream_url = refererResolver(video)
            if stream_url == False:
                  return                                                            
            infoL={'Title': infoLabels['title'], 'Plot': infoLabels['plot'], 'Genre': infoLabels['genre'], 'originaltitle': infoLabels['metaName']}
            # play with bookmark
            stream_url=stream_url.replace(' ','%20')
            player = playbackengine.PlayWithoutQueueSupport(resolved_url=stream_url, addon_id=addon_id, video_type=video_type, title=str(infoLabels['title']),season=str(season), episode=str(episode), year=str(infoLabels['year']),img=img,infolabels=infoL, watchedCallbackwithParams=main.WatchedCallbackwithParams,imdb_id=imdb_id)
            #WatchHistory
            if selfAddon.getSetting("whistory") == "true":
                wh.add_item(mname+' '+'[COLOR green]VIPlaylist[/COLOR]', sys.argv[0]+sys.argv[2], infolabels=infolabels, img=img, fanart=fanart, is_folder=False)
            player.KeepAlive()
            return ok
        except Exception, e:
                if stream_url != False:
                        main.ErrorReport(e)
                return ok


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

def unescape(text):
        try:            
            rep = {"&nbsp;": " ",
                   "\n": "",
                   "\t": "",   
                   "%3a": ":",
                   "%3A":":",
                   "%2f":"/",
                   "%2F":"/",
                   "%3f":"?",
                   "%3F":"?",
                   "%26":"&",
                   "%3d":"=",
                   "%3D":"=",
                   "%2C":",",
                   "%2c":","
                   }
            for s, r in rep.items():
                text = text.replace(s, r)
				
            # remove html comments
            text = re.sub(r"<!--.+?-->", "", text)    
				
        except TypeError:
            pass

        return text

def LIST(murl):
        link=main.OPENURL(murl)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace("type='text'>Pencuri Movie</title>",'')
        match= re.compile("""<title type='text'>([^<]+)</title><.+?>.+?div class=".+?" style=".+?".+?href="(.+?)" imageanchor=".+?" .+?href='.+?'.+?href='([^<]+).html' title='.+?'/><author>""").findall(link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Movie list is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0,'[B]Will load instantly from now on[/B]',remaining_display)
        for name,thumb,url in match:
                f=re.findall('One Piece',name)
                r=re.findall('Streaming',name)
                if len(f)==0 and len(r)==0:
                    main.addPlayM(name,url+'.html',216,thumb,'','','','','')
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
                if (dialogWait.iscanceled()):
                        return False   
        dialogWait.close()
        del dialogWait
        main.GA("HD","Pencurimovie")

def LINK(mname,url,thumb):
        main.GA("Pencurimovie","Watched")
        ok=True
        namelist=[]
        urllist=[]
        infoLabels =main.GETMETAT(mname,'','',thumb)
        video_type='movie'
        season=''
        episode=''
        img=infoLabels['cover_url']
        fanart =infoLabels['backdrop_url']
        imdb_id=infoLabels['imdb_id']
        infolabels = { 'supports_meta' : 'true', 'video_type':video_type, 'name':str(infoLabels['title']), 'imdb_id':str(infoLabels['imdb_id']), 'season':str(season), 'episode':str(episode), 'year':str(infoLabels['year']) }
        link=main.OPENURL(url)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        docUrl= re.compile('<iframe height=".+?" src="(.+?)" width=".+?"></iframe>').findall(link)
        if docUrl:
            link2=main.OPENURL(docUrl[0])
            match= re.compile('url_encoded_fmt_stream_map\":\"(.+?),\"').findall(link2)
            if match:
                streams_map = str(match)
                stream= re.compile('url=(.+?)&type=.+?&quality=(.+?)[,\"]{1}').findall(streams_map)
                for group1,group2 in stream:#Thanks to the-one for google-doc resolver
                    stream_url = str(group1)
                    stream_url = unescape(stream_url)
                    urllist.append(stream_url)
                    stream_qlty = str(group2.upper())
                    if (stream_qlty == 'HD720'):
                        stream_qlty = 'HD-720p'
                    elif (stream_qlty == 'LARGE'):
                        stream_qlty = 'SD-480p'
                    elif (stream_qlty == 'MEDIUM'):
                        stream_qlty = 'SD-360p'
                    namelist.append(stream_qlty)
                dialog = xbmcgui.Dialog()
                answer =dialog.select("Quality Select", namelist)
                if answer != -1:
                        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Opening Link,3000)")
                        stream_url2 = urllist[int(answer)]
                        infoL={'Title': infoLabels['title'], 'Plot': infoLabels['plot'], 'Genre': infoLabels['genre']}
                        # play with bookmark
                        player = playbackengine.PlayWithoutQueueSupport(resolved_url=stream_url2, addon_id=addon_id, video_type=video_type, title=str(infoLabels['title']),season=str(season), episode=str(episode), year=str(infoLabels['year']),img=img,infolabels=infoL, watchedCallbackwithParams=main.WatchedCallbackwithParams,imdb_id=imdb_id)
                        #WatchHistory
                        if selfAddon.getSetting("whistory") == "true":
                            wh.add_item(mname+' '+'[COLOR green]Pencurimovie[/COLOR]', sys.argv[0]+sys.argv[2], infolabels=infolabels, img=img, fanart=fanart, is_folder=False)
                        player.KeepAlive()
                        return ok
                else:
                    return ok
        vidmUrl= re.compile('<iframe frameborder=".+?" height=".+?" scrolling=".+?" src="(.+?)" width=".+?"></iframe>').findall(link)
        if vidmUrl:
                link2=main.OPENURL(vidmUrl[0])
                xbmc.executebuiltin("XBMC.Notification(Please Wait!,Opening Link,3000)")
                encodedurl=re.compile('unescape.+?"(.+?)"').findall(link2)#Thanks to j0anita for vidmega resolver
                teste=urllib.unquote(encodedurl[0])
                mega=re.compile('file: "(.+?)"').findall(teste)
                for url in mega:
                        stream_url = url
                        infoL={'Title': infoLabels['title'], 'Plot': infoLabels['plot'], 'Genre': infoLabels['genre']}
                        # play with bookmark
                        player = playbackengine.PlayWithoutQueueSupport(resolved_url=stream_url2, addon_id=addon_id, video_type=video_type, title=str(infoLabels['title']),season=str(season), episode=str(episode), year=str(infoLabels['year']),img=img,infolabels=infoL, watchedCallbackwithParams=main.WatchedCallbackwithParams,imdb_id=imdb_id)
                        #WatchHistory
                        if selfAddon.getSetting("whistory") == "true":
                            wh.add_item(mname+' '+'[COLOR green]Pencurimovie[/COLOR]', sys.argv[0]+sys.argv[2], infolabels=infolabels, img=img, fanart=fanart, is_folder=False)
                        player.KeepAlive()
                        return ok
        
        else:
            xbmc.executebuiltin("XBMC.Notification(Sorry!,Link Not Available,3000)")
            return ok


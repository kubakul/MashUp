import urllib,urllib2,re,cookielib,sys,os
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
from resources.libs import main

#Mash Up - by Mash2k3 2012.

from t0mm0.common.addon import Addon
addon_id = 'plugin.video.movie25'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon('plugin.video.movie25', sys.argv)
art = main.art
from universal import watchhistory
    
wh = watchhistory.WatchHistory('plugin.video.movie25')



def VIPplaylists(murl):
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
            main.addDirc(name+' [COLOR red] Updated '+date+'[/COLOR]',url,182,thumb,'',fan,'','','')
        info=re.findall('<info><message>(.+?)</message><thumbnail>(.+?)</thumbnail></info>',link)
        if info:
            for msg,pic in info:
                main.addLink(msg,'',pic)
        popup=re.compile('<popup><name>([^<]+)</name.+?popImage>([^<]+)</popImage.+?thumbnail>([^<]+)</thumbnail></popup>').findall(link)
        for name,image,thumb in popup:
                main.addPlayc(name,image,244,thumb,'','','','','')
        main.GA("Live",vip+"-Playlists")


def VIPList(mname,murl):
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
                main.addPlayc(name,image,244,thumb,'','','','','')
        directory=re.compile('<dir><name>([^<]+)</name.+?link>([^<]+)</link.+?thumbnail>([^<]+)</thumbnail></dir>').findall(link)
        for name,url,thumb in directory:
                main.addDir(name,url,236,thumb)
        match=re.compile('<title>([^<]+)</title.+?link>(.+?)</link.+?thumbnail>([^<]+)</thumbnail>').findall(link)
        for name,url,thumb in sorted(match):
            main.addPlayL(name+' [COLOR blue]'+vip+'[/COLOR]',url,183,thumb,'',fan,'','','')
        main.GA(vip+"-Playlists",mname)

def VIPLink(mname,murl,thumb):
        main.GA(mname,"Watched")
        ok=True
        namelist=[]
        urllist=[]
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        match=re.compile('<sublink>(.+?)</sublink>').findall(murl)
        if match:
                i=1
                for url in match:
                        name= 'Link '+str(i)
                        namelist.append(name)        
                        urllist.append(url)
                        i=i+1
                dialog = xbmcgui.Dialog()
                answer =dialog.select("Pick A Link", namelist)
                if answer != -1:
                        murl=urllist[int(answer)]
                        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Opening Link,5000)")
                else:
                      return  
        stream_url = murl
        listitem = xbmcgui.ListItem(thumbnailImage=thumb)
        listitem.setInfo('video', {'Title': mname, 'Genre': 'Live'} )
        
        playlist.add(stream_url,listitem)
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(playlist)
        #WatchHistory
        if selfAddon.getSetting("whistory") == "true":
            wh.add_item(mname+' '+'[COLOR green]Live[/COLOR]', sys.argv[0]+sys.argv[2], infolabels='', img=thumb, fanart='', is_folder=False)
        return ok

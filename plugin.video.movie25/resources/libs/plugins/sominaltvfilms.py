import urllib,urllib2,re,cookielib,string, urlparse,sys,os
import xbmc, xbmcgui, xbmcaddon, xbmcplugin,urlresolver
from t0mm0.common.net import Net as net
from t0mm0.common.addon import Addon
from resources.libs import main
from decimal import Decimal
import time

#Mash Up - by Mash2k3 2012.

from t0mm0.common.addon import Addon
from universal import playbackengine, watchhistory
addon_id = 'plugin.video.movie25'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon('plugin.video.movie25', sys.argv)
art = main.art
datapath = addon.get_profile()


    
wh = watchhistory.WatchHistory('plugin.video.movie25')


def MAIN():
        main.GA("Plugin","SominalTv")
        main.addDir('Search','xoxe',624,art+'/search.png')
        main.addDir('Hindi','http://www.sominaltvfilms.com/category/hindi-movies',620,art+'/wfs/hindi.png')
        main.addDir('Telugu','http://www.sominaltvfilms.com/category/telugu',620,art+'/wfs/telugu.png')
        main.addDir('Tamil','http://www.sominaltvfilms.com/category/tamil',620,art+'/wfs/tamil.png')
        main.addDir('Malayalam','http://www.sominaltvfilms.com/category/malayalam',620,art+'/wfs/malayalam.png')
        main.addDir('Punjabi','http://www.sominaltvfilms.com/category/punjabi',620,art+'/wfs/punjabi.png')
        main.addDir('BluRay','http://www.sominaltvfilms.com/category/bluray',620,art+'/wfs/bluray.png')
        main.addDir('All English Subtitled Movies','http://www.sominaltvfilms.com/category/english-subtitled',620,art+'/wfs/subtitled.png')
        main.addDir('All Hindi Dubbed Movies','http://www.sominaltvfilms.com/category/hindi-dubbed',620,art+'/wfs/dubbed.png')


def AtoZ(url):
    main.addDir('0-9','http://www.sominaltvfilms.com/search/label/%23'+url+'?&max-results=15',620,art+'/wfs/09.png')
    for i in string.ascii_uppercase:
            main.addDir(i,'http://www.sominaltvfilms.com/search/label/'+i+url+'?&max-results=15',620,art+'/wfs/'+i+'.png')
    main.GA("Watchseries","A-Z")
    main.VIEWSB()
    
def SEARCH():
        keyb = xbmc.Keyboard('', 'Search Movies')
        keyb.doModal()
        if (keyb.isConfirmed()):
                search = keyb.getText()
                encode=urllib.quote(search)
                surl='http://www.sominaltvfilms.com/?s='+encode
        link=main.OPENURL(surl)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile('<img width=".+?" height=".+?" src="(.+?)" class=".+?" alt=".+?".+?<h1 class=".+?"><a class=".+?" href="(.+?)" title=".+?">(.+?)</a></h1>.+?<div class="excerpt-wrapper"><div class="excerpt"><p>(.+?)</p>').findall(link)
        for thumb,url,name,desc in match:
            desc=desc.replace('</div><div class="separator" style="clear: both; text-align: left;">','').replace('<span class="Apple-style-span" style="background-color: white; color: #333333; font-family: Verdana, Arial, sans-serif; font-size: 13px; line-height: 18px;">','').replace('</div><div class="separator" style="clear: both; text-align: justify;">','').replace('</div><div class="separator" style="clear: both; text-align: center;">','').replace('</span>','').replace('<span>','').replace('</div><div class="separator" style="clear: both; text-align: justify;"><span class="Apple-style-span" style="background-color: white; color: #333333; font-family: Verdana, Arial, sans-serif; font-size: 13px; line-height: 18px;">','')
            desc=desc.replace('<br>','').replace('</br>','').replace('</div>','').replace('<div>','')
            main.addDirM(name,url,621,thumb,desc,thumb,'','','')

               

def LIST(mname,murl):
        main.GA("SominalTv","List")
        if mname=='Hindi':
                main.addDir('Hindi English Subtitled','http://www.sominaltvfilms.com/category/hindi-movies-english-subtitles',620,art+'/wfs/subtitled.png')
                main.addDir('Hindi BluRay','http://www.sominaltvfilms.com/category/hindi-blurays',620,art+'/wfs/bluray.png')
        elif mname=='Telugu':
                main.addDir('Telugu English Subtitled','http://www.sominaltvfilms.com/category/telugu-movies-english-subtitles',620,art+'/wfs/subtitled.png')
                main.addDir('Telugu BluRay','http://www.sominaltvfilms.com/category/telugu-blurays',620,art+'/wfs/bluray.png')
        elif mname=='Tamil':
                main.addDir('Tamil English Subtitled','http://www.sominaltvfilms.com/category/tamil-movies-english-subtitles',620,art+'/wfs/subtitled.png')
                main.addDir('Tamil BluRay','http://www.sominaltvfilms.com/category/tamil-blurays',620,art+'/wfs/bluray.png')
        elif mname=='Malayalam':
                main.addDir('Malayalam English Subtitled','http://www.sominaltvfilms.com/category/malayalam-movies-english-subtitles',620,art+'/wfs/subtitled.png')
        elif mname=='Punjabi':
                main.addDir('Punjabi English Subtitled','http://www.sominaltvfilms.com/category/punjabi-movies-english-subtitles',620,art+'/wfs/subtitled.png')
        elif mname=='All Hindi Dubbed Movies':
                main.addDir('Dubbed BluRay','http://www.sominaltvfilms.com/category/hindi-dubbed-blurays',620,art+'/wfs/bluray.png')
        link=main.OPENURL(murl)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile('<img width=".+?" height=".+?" src="(.+?)" class=".+?" alt=".+?/></a></div></center><div class=".+?"><h2 class=".+?"><a class=".+?" href="(.+?)" title=".+?">(.+?)</a></h2><div class="excerpt">(.+?)...</div>').findall(link)
        dialogWait = xbmcgui.DialogProgress()
        ret = dialogWait.create('Please wait until Show list is cached.')
        totalLinks = len(match)
        loadedLinks = 0
        remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
        dialogWait.update(0,'[B]Will load instantly from now on[/B]',remaining_display)
        for thumb,url,name,desc in match:
                desc=desc.replace('  ','')
                main.addDirM(name,url,621,thumb,desc,thumb,'','','')
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                remaining_display = 'Movies loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B].'
                dialogWait.update(percent,'[B]Will load instantly from now on[/B]',remaining_display)
                if (dialogWait.iscanceled()):
                    return False   
        dialogWait.close()
        del dialogWait
        paginate = re.compile("""<a href="([^<]+)">Next &rsaquo;</a>""").findall(link)
        if len(paginate)>0:
            main.addDir('Next',paginate[0],620,art+'/next2.png')
        main.VIEWS()

def LINK(manme,murl,thumb,fan,desc):
        link=main.OPENURL(murl)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match= re.compile('<a href="http://adf.ly/377117/(.+?)".+?target="_blank.+?>(.+?)</a>').findall(link)

        for url,name in match:
            name=name.replace('</b>','').replace('<b>','').replace('<span style="font-size: x-large;">','').replace('<span id="goog_1857978069"></span><span id="goog_1857978070"></span>','').replace('<span style="font-family: Verdana, sans-serif; font-size: x-large;">','').replace('<span style="font-family: Verdana, sans-serif; font-size: large;">','').replace('<span>','').replace('</span>','')
            http= re.compile('http://').findall(url)
            if len(http)==0:
                url='http://'+url
            main.addPlayc(name,url,622,thumb,desc,fan,'','','')
    

def LINK2(mname,murl,thumb,desc):
       
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
        link2=main.OPENURL(murl)
        SRT=os.path.join(datapath,'Sub.srt')
        if  os.path.exists(SRT):
                os.remove(SRT)
        link2=link2.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        docUrl= re.compile('iframe src="(.+?)"').findall(link2)
        if len(docUrl)==0:
            link3=dekode(link2)
            try:
                    docUrl= re.compile('iframe src="(.+?)"').findall(link3)
            except:
                youtube= re.compile('<iframe width=".+?" height=".+?" src="http://www.youtube.com/embed/(.+?)" scrolling=".+?"').findall(link2)
                url = "plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid="+youtube[0]+"&hd=1"
                stream_url = url
                # play with bookmark
                player = playbackengine.PlayWithoutQueueSupport(resolved_url=stream_url, addon_id=addon_id, video_type='', title=mname,season='', episode='', year='',img=thumb,infolabels='', watchedCallbackwithParams=main.WatchedCallbackwithParams,imdb_id='')
                #WatchHistory
                if selfAddon.getSetting("whistory") == "true":
                    wh.add_item(mname+' '+'[COLOR green]SominalFilms[/COLOR]', sys.argv[0]+sys.argv[2], infolabels='', img=thumb, fanart='', is_folder=False)
                player.KeepAlive()
                return ok

        

        if docUrl:
                
                xbmc.executebuiltin("XBMC.Notification(Please Wait!,Collecting Links,3000)")
                link2=main.OPENURL(docUrl[0])
                link2=link2.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\/','/').replace('\\','')
                match= re.compile('url_encoded_fmt_stream_map\":\"(.+?),\"').findall(link2)
                if match:
                        subtitle_url_start= re.compile("\"ttsurl\":\"(.+?)\"").findall(link2)
                        v_add= re.compile("id=(.+?)&").findall(subtitle_url_start[0])
                        subtitle_url_start = subtitle_url_start[0] + '&v=' + v_add[0]
                        subtitle_url_start = subtitle_url_start + '&name=(www.SominalTvFilms.com)&lang=en&hl=e&format=1&type=track&kind'
                        print "Subtitle File="+str(subtitle_url_start)
                        #Converts Xml file to SRT file
                        try:
                                link=main.OPENURL(subtitle_url_start)
                                link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('<text start="0">','')
                        except:
                                link=''
                        
                        submatch= re.compile('<text start="(.+?)" dur="(.+?)">(.+?)</text>').findall(link)
                        if submatch:
                                i=1
                                for start,dur,text in submatch:
                                        #Converts seconds to HH:MM:SS,MS format for srt file
                                        text=text.replace('&#39;',"'").replace('&quot;','"').replace('&amp;',"&").replace("&#39;","'").replace('&lt;i&gt;','').replace("#8211;","-").replace('&lt;/i&gt;','').replace("&#8217;","'").replace('&amp;quot;','"').replace('&#215;','').replace('&#038;','').replace('&#8216;','').replace('&#8211;','').replace('&#8220;','').replace('&#8221;','').replace('&#8212;','')
                                        dur=Decimal(start)+Decimal(dur)
                                        dur=str(dur)
                                        if(float(start)%1 != 0):
                                                start1=start.split('.')[0]
                                                start2=start.split('.')[1]
                                        else:
                                                start1=start
                                                start2=0
                                        start = time.strftime('%H:%M:%S', time.gmtime(float(start1)))
                                        if(float(dur)%1 != 0):
                                                dur1=dur.split('.')[0]
                                                dur2=dur.split('.')[1]
                                        else:
                                                dur1=dur
                                                dur2=0
                                        dur = time.strftime('%H:%M:%S', time.gmtime(float(dur1)))
                                        #creating srt file and saving it on mashup profile folder
                                        open(SRT,'a').write("""
"""+str(i)+"""
"""+str(start)+","+str(start2)+" --> "+str(dur)+","+str(dur2)+"""
"""+text+"""
""") 
                                        i=i+1

                        streams_map = str(match)
                        stream= re.compile('url=(.+?)&type=.+?&quality=(.+?)[,\"]{1}').findall(streams_map)
                        for group1,group2 in stream:#Thanks to the-one for google-doc resolver
                                stream_url = str(group1)
                                stream_url = main.unescapes(stream_url)
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
                                main.GA("SominalTv","Watched")
                                xbmc.executebuiltin("XBMC.Notification(Please Wait!,Opening Link,3000)")
                                stream_url2 = urllist[int(answer)]
                                infoL={'Title': infoLabels['title'], 'Plot': infoLabels['plot'], 'Genre': infoLabels['genre']}
                                # play with bookmark
                                player = playbackengine.PlayWithoutQueueSupport(resolved_url=stream_url, addon_id=addon_id, video_type=video_type, title=str(infoLabels['title']),season=str(season), episode=str(episode), year=str(infoLabels['year']),img=img,infolabels=infoL, watchedCallbackwithParams=main.WatchedCallbackwithParams,imdb_id=imdb_id)
                                player.setSubtitles(SRT)#inserts Srt file from profile folder
                                main.GA("SominalTv","Watched")
                                #WatchHistory
                                if selfAddon.getSetting("whistory") == "true":
                                    wh.add_item(mname+' '+'[COLOR green]SominalFilms[/COLOR]', sys.argv[0]+sys.argv[2], infolabels='', img=thumb, fanart='', is_folder=False)
                                player.KeepAlive()
                                 

                        return ok
        else:
                        xbmc.executebuiltin("XBMC.Notification(Sorry!,Protected Link,5000)")




def _enk_dec_num(kode, enc):
    if re.search('fromCharCode', enc):
        x = ''
        for nbr in kode.split():
            x += chr(int(nbr) - 3)
        return x
    else:
        return None
    
def _enk_dec_swap(kode, enc):
    if re.search('charAt', enc):
        x = ''
        i = 0
        while i < (len(kode) - 1):
            x += (kode[i + 1] + kode[i])
            i += 2
        return (x + (kode[len(kode) - 1] if i < len(kode) else ''))
    else:
        return None
    
def _enk_dec_reverse(kode, enc):
    if re.search('reverse', enc):
        return kode[::-1]
    else:
        return None
    
ENK_DEC_FUNC = [_enk_dec_num, _enk_dec_swap, _enk_dec_reverse]


def dekode(html):
    kodeParts = re.compile('var kode\="kode\=\\\\"(.+?)\\\\";(.+?);"').findall(html)
    if len(kodeParts) == 0:
        return None
    kode = None
    while len(kodeParts) == 1:
        kode = kodeParts[0][0].replace('BY_PASS_D', '"').replace('BY_PASS_S', '\'').replace('\\\\', '\\')
        enc = kodeParts[0][1].replace('BY_PASS_D', '"').replace('BY_PASS_S', '\'').replace('\\\\', '\\')
        for dec_func in ENK_DEC_FUNC:
            x = dec_func(kode, enc)
            if x is not None:
                kode = x
        kodeParts = re.compile('kode\="(.+?)";(.*)').findall(kode.replace('\\"', 'BY_PASS_D').replace('\\\'', 'BY_PASS_S'))
    dekoded = kode.replace('\\"', '"').replace('\\\'', '\'').replace('\\\\', '\\')
    return dekoded            

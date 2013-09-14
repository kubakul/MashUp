import urllib,urllib2,re,cookielib,os,sys
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
from resources.libs import main
from urllib2 import (urlopen, Request)
from BeautifulSoup import BeautifulSoup

#Mash Up - by Mash2k3 2012.

from t0mm0.common.addon import Addon
addon_id = 'plugin.video.movie25'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon('plugin.video.movie25', sys.argv)
art = main.art
from universal import watchhistory
    
wh = watchhistory.WatchHistory('plugin.video.movie25')

def get(url):
    """Performs a GET request for the given url and returns the response"""
    try:
        conn = urlopen(url)
        resp = conn.read()
        conn.close()
        return resp
    except IOError:
        pass
    return ""

def _html(url):
    """Downloads the resource at the given url and parses via BeautifulSoup"""
    return BeautifulSoup(main.OPENURL(url), convertEntities=BeautifulSoup.HTML_ENTITIES)

def _parse_channels_from_html_dom(html):
    items = []

    for div in html.findAll("div", {"class": "div_channel"}):
        match2=re.compile('''<a href=".+?" onclick="go_c2.?'(.+?)'.+?'rtmp.+?'.?" style_=".+?"><img onerror=".+?" src="(.+?)" height=".+?" style=".+?" /><font style=".+?"> <span id=".+?">(.+?)</span> <font style=".+?">(.+?)</font>''').findall(str(div))
        match=re.compile('''<a href=".+?" onclick="go_c2.?'(.+?)'.+?'rtmp.+?'.?" style_=".+?"><img onerror=".+?" src="(.+?)" height=".+?" style=".+?" /><font style=".+?"> <span id=".+?">(.+?)</span>''').findall(str(div))
        for url,thumb,name in match:
            for url2,thumb2,name2,hd in match2:
                if name==name2:
                    name=name+' [COLOR red]HD[/COLOR]'
        items.append({
            'title': name,
            'thumbnail': thumb,
            'path': url
        })
    items.append({
            'title': 'MBC 3',
            'thumbnail': 'https://upload.wikimedia.org/wikipedia/ar/c/c8/Mbc_3_logo_not_2_1_4_action-%D8%B5%D9%88%D8%B1%D8%A9-file.jpg',
            'path': 'mbc_3'})
    items.append({
            'title': 'MBC',
            'thumbnail': 'https://si0.twimg.com/profile_images/1133033554/mbc-fb.JPG',
            'path': 'mbc_1'})
    items.append({
            'title': 'MBC 2',
            'thumbnail': 'https://si0.twimg.com/profile_images/2325153399/glxj6ox08i7xhuwfop44.jpeg',
            'path': 'mbc_2'})
    items.append({
            'title': 'MBC 4',
            'thumbnail': 'https://si0.twimg.com/profile_images/1133002857/mbc4.jpg',
            'path': 'mbc_4'})
    items.append({
            'title': 'JSC +1',
            'thumbnail': 'http://nowwatchtvlive.com/wp-content/uploads/2011/07/AljazeeraSport-264x300.jpg',
            'path': 'jsc_1'})
    items.append({
            'title': 'JSC +2',
            'thumbnail': 'http://nowwatchtvlive.com/wp-content/uploads/2011/07/AljazeeraSport-264x300.jpg',
            'path': 'jsc_2'})
    items.append({
            'title': 'JSC +3',
            'thumbnail': 'http://nowwatchtvlive.com/wp-content/uploads/2011/07/AljazeeraSport-264x300.jpg',
            'path': 'jsc_3'})
    items.append({
            'title': 'JSC +4',
            'thumbnail': 'http://nowwatchtvlive.com/wp-content/uploads/2011/07/AljazeeraSport-264x300.jpg',
            'path': 'jsc_4'})
    items.append({
            'title': 'JSC +5',
            'thumbnail': 'http://nowwatchtvlive.com/wp-content/uploads/2011/07/AljazeeraSport-264x300.jpg',
            'path': 'jsc_5'})
    items.append({
            'title': 'JSC +6',
            'thumbnail': 'http://nowwatchtvlive.com/wp-content/uploads/2011/07/AljazeeraSport-264x300.jpg',
            'path': 'jsc_6'})
    items.append({
            'title': 'JSC +7',
            'thumbnail': 'http://nowwatchtvlive.com/wp-content/uploads/2011/07/AljazeeraSport-264x300.jpg',
            'path': 'jsc_7'})
    items.append({
            'title': 'JSC +8',
            'thumbnail': 'http://nowwatchtvlive.com/wp-content/uploads/2011/07/AljazeeraSport-264x300.jpg',
            'path': 'jsc_8'})
    items.append({
            'title': 'JSC +9',
            'thumbnail': 'http://nowwatchtvlive.com/wp-content/uploads/2011/07/AljazeeraSport-264x300.jpg',
            'path': 'jsc_9'})
    items.append({
            'title': 'JSC +10',
            'thumbnail': 'http://nowwatchtvlive.com/wp-content/uploads/2011/07/AljazeeraSport-264x300.jpg',
            'path': 'jsc_10'})
    items.append({
            'title': 'Abu Dhabi Al Oula',
            'thumbnail': 'https://www.zawya.com/pr/images/2009/ADTV_One_RGB_2009_10_08.jpg',
            'path': 'abu_dhabi'})
    items.append({
            'title': 'Abu Dhabi Sports',
            'thumbnail': 'https://si0.twimg.com/profile_images/2485587448/2121.png',
            'path': 'abu_dhabi_sports_1'})
    items.append({
            'title': 'Al Jazeera',
            'thumbnail': 'http://www.chicagonow.com/chicago-sports-media-watch/files/2013/04/Al-Jazeera.jpg',
            'path': 'aljazeera'})
    items.append({
            'title': 'JAl Jazeera Sport 1',
            'thumbnail': 'http://nowwatchtvlive.com/wp-content/uploads/2011/07/AljazeeraSport-264x300.jpg',
            'path': 'aljazeera_sport_1'})
    items.append({
            'title': 'Al Jazeera Sport 2',
            'thumbnail': 'http://nowwatchtvlive.com/wp-content/uploads/2011/07/AljazeeraSport-264x300.jpg',
            'path': 'aljazeera_sport_2'})
    items.append({
            'title': 'Al Jazeera Mubasher Masr',
            'thumbnail': 'http://www.chicagonow.com/chicago-sports-media-watch/files/2013/04/Al-Jazeera.jpg',
            'path': 'aljazeera_mubasher_masr'})
    items.append({
            'title': 'Al Jazeera Children',
            'thumbnail': 'http://www.chicagonow.com/chicago-sports-media-watch/files/2013/04/Al-Jazeera.jpg',
            'path': 'aljazeera_children'})
    
    return items

def MAIN():
    main.GA("Live","ArabicStreams")
    html = _html('http://www.teledunet.com/')
    items = _parse_channels_from_html_dom(html)
    for channels in sorted(items):
        main.addPlayL(channels['title'],channels['path'],232,channels['thumbnail'],'','','','','')
        

def _get_channel_time_player(channel_name):
    url = 'http://www.teledunet.com/tv/?channel=%s&no_pub' % channel_name
    req = Request(url)
    req.add_header('Referer', 'http://www.teledunet.com/')    # Simulate request is coming from website
    html = get(req)

    m = re.search('time_player=(.*);', html, re.M | re.I)
    time_player_str = eval(m.group(1))
    

    m = re.search('curent_media=\'(.*)\';', html, re.M | re.I)
    rtmp_url = m.group(1)
    play_path= rtmp_url[rtmp_url.rfind("/")+1:]
    tpID=repr(time_player_str).rstrip('0').rstrip('.')
    swfUrl='swfUrl=http://www.teledunet.com/tv/player.swf?bufferlength=5&repeat=single&autostart=true&id0=%s&streamer=%s&file=%s&provider=rtmp' %(tpID, rtmp_url, play_path, )
    return rtmp_url+' app=teledunet '+swfUrl+' playpath='+play_path+' live=1 timeout=15 pageUrl='+url


        
def LINK(mname,url,thumb):
        main.GA("ArabicStreams","Watched")
        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Opening Stream,3000)")
        stream_url = _get_channel_time_player(url)
        ok=True
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        
        listitem = xbmcgui.ListItem(thumbnailImage=thumb)
        listitem.setInfo('video', {'Title': mname, 'Genre': 'Live'} )
        
        playlist.add(stream_url,listitem)
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(playlist)
        #WatchHistory
        if selfAddon.getSetting("whistory") == "true":
            wh.add_item(mname+' '+'[COLOR green]ArabicStreams[/COLOR]', sys.argv[0]+sys.argv[2], infolabels='', img=thumb, fanart='', is_folder=False)
        return ok




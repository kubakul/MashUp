import urllib,urllib2,re,cookielib,string
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
from t0mm0.common.net import Net
net = Net()
from resources.libs import main
art = main.art
search = {}
def searchm25(encode):
    
    surl='http://www.movie25.so/search.php?key='+encode+'&submit='
    link=main.OPENURL(surl)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
    match=re.compile('<div class="movie_pic"><a href="(.+?)" target=".+?">    <img src="(.+?)" width=".+?" height=".+?" />.+?<a href=".+?" target=".+?">(.+?)</a></h1><div class=".+?">').findall(link)
    for url,thumb,name in match:
            search['name'] = name
            search['url'] = url
            search['thumb'] = thumb
    print search

def searchiwo(encode):
    search_url = 'http://www.iwatchonline.to/search'
    search_content = net.http_POST(search_url, { 'searchquery' : encode, 'searchin' : 'm'} ).content
    r = re.findall('(?s)<table(.+?)</table>',search_content)
    r=main.unescapes(r[0])
    match=re.compile('<img.+?src=\"(.+?)\".+?<a.+?href=\"(.+?)\">(.+?)</a>').findall(r)
    for thumb,url,name in match:
            search['name'] = name
            search['url'] = url
            search['thumb'] = thumb
    return search

def searchmnv(encode):
    surl='http://www.myvideolinks.eu/index.php?s='+encode
    link=main.OPENURL(surl)
    link=main.unescapes(link)
    match=re.compile("""<a href=".+?" rel=".+?" title=".+?"> <img src="(.+?)" width=".+?" height=".+?" title="(.+?)" class=".+?"></a><h4><a href="(.+?)" rel""").findall(link)
    for thumb,name,url in match:
        if not re.findall('HDTV',name):
            search['name'] = name
            search['url'] = url
            search['thumb'] = thumb
    return search


def SuperSearch():
        keyb = xbmc.Keyboard('', 'Search For Shows or Episodes')
        keyb.doModal()
        if (keyb.isConfirmed()):
                search = keyb.getText()
                encode=urllib.quote(search)
        m25=searchm25(encode)
        print m25
        if m25:
            iwo=searchiwo(encode)
            z = m25.update(iwo)
            if z:
                mnv=searchmnv(encode)
                z = z.update(mnv)
        print z

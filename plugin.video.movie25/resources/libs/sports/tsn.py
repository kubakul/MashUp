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


def TSNDIR():
        main.addDir('Featured','http://esi.ctv.ca/datafeedrss/vhBinData.aspx?bid=14070',97,art+'/tsn.png')
        main.addDir('NHL','nhl',96,art+'/tsn.png')
        main.addDir('NFL','nfl',96,art+'/tsn.png')
        main.addDir('NBA','nba',96,art+'/tsn.png')
        main.addDir('Hockey Canada','canadian_hockey',96,art+'/tsn.png')
        main.addDir('CFL','cfl',96,art+'/tsn.png')
        main.addDir('MLB','mlb',96,art+'/tsn.png')
        main.addDir('Soccer','soccer',96,art+'/tsn.png')
        main.addDir('Curling','http://esi.ctv.ca/datafeedrss/vhBinData.aspx?bid=1524',97,art+'/tsn.png')
        main.addDir('Golf','http://esi.ctv.ca/datafeedrss/vhBinData.aspx?bid=1126',97,art+'/tsn.png')
        main.addDir('Tennis','http://esi.ctv.ca/datafeedrss/vhBinData.aspx?bid=1124',97,art+'/tsn.png')
        main.addDir('NLL','http://esi.ctv.ca/datafeedrss/vhBinData.aspx?bid=5995',97,art+'/tsn.png')
        main.addDir('X Games','http://esi.ctv.ca/datafeedrss/vhBinData.aspx?bid=3133',97,art+'/tsn.png')
        main.addDir('TSN Shows','shows',96,art+'/tsn.png')
        main.addDir('MMA','http://esi.ctv.ca/datafeedrss/vhBinData.aspx?bid=1134',97,art+'/tsn.png')
        main.addDir('NCAA','http://esi.ctv.ca/datafeedrss/vhBinData.aspx?bid=9981',97,art+'/tsn.png')
        main.GA("Sports","TSN")


def TSNDIRLIST(murl):
        thumb=art+'/folder.png'
        if murl=='nhl':
            main.addDir('Latest','http://esi.ctv.ca/datafeedrss/vhBinData.aspx?bid=1104',97,thumb)
            main.addDir('Highlights','http://esi.ctv.ca/datafeedrss/vhSportEventClips.aspx?leagueId=1&categoryId=1&binId=1104',97,thumb)
            main.addDir('News & Analysis','http://esi.ctv.ca/datafeedrss/vhSportEventClips.aspx?leagueId=1&categoryId=3&binId=1104',97,thumb)
            main.addDir('Features','http://esi.ctv.ca/datafeedrss/vhSportEventClips.aspx?leagueId=1&categoryId=4&binId=1104',97,thumb)
            main.addDir("That's Hockey",'http://esi.ctv.ca/datafeedrss/vhBinData.aspx?bid=2452',97,thumb)
            main.addDir('TH2N','http://esi.ctv.ca/datafeedrss/vhBinData.aspx?bid=9598',97,thumb)
            main.addDir('Top 50 NHL Players','http://esi.ctv.ca/datafeedrss/vhBinData.aspx?bid=16230',97,thumb)
            main.addLink('TEAM CHANNELS','','')
            main.addDir('Canucks','http://esi.ctv.ca/datafeedrss/vhSportEventClips.aspx?teamId=28&binId=1104',97,'http://images.tsn.ca/images/v3/logos/24x24/nhl-canucks.png')
            main.addDir('Flames','http://esi.ctv.ca/datafeedrss/vhSportEventClips.aspx?teamId=4&binId=1104',97,'http://images.tsn.ca/images/v3/logos/24x24/nhl-flames.png')
            main.addDir('Oilers','http://esi.ctv.ca/datafeedrss/vhSportEventClips.aspx?teamId=11&binId=1104',97,'http://images.tsn.ca/images/v3/logos/24x24/nhl-oilers.png')
            main.addDir('Jets','http://esi.ctv.ca/datafeedrss/vhSportEventClips.aspx?teamId=30&binId=1104',97,'http://images.tsn.ca/images/v3/logos/24x24/nhl-jets.png')
            main.addDir('Maple Leafs','http://esi.ctv.ca/datafeedrss/vhSportEventClips.aspx?teamId=27&binId=1104',97,'http://images.tsn.ca/images/silver/_fpos/toronto_maple_leafs.png')
            main.addDir('Senators','http://esi.ctv.ca/datafeedrss/vhSportEventClips.aspx?teamId=20&binId=1104',97,'http://images.tsn.ca/images/v3/logos/24x24/nhl-senators.png')
            main.addDir('Canadiens','http://esi.ctv.ca/datafeedrss/vhSportEventClips.aspx?teamId=15&binId=1104',97,'http://images.tsn.ca/images/v3/logos/24x24/nhl-canadiens.png')

        elif murl=='nfl':
            main.addDir('Latest','http://esi.ctv.ca/datafeedrss/vhBinData.aspx?bid=1175',97,thumb)
            main.addDir('Highlights','http://esi.ctv.ca/datafeedrss/vhSportEventClips.aspx?leagueId=9&categoryId=1&binId=1175',97,thumb)
            main.addDir('News & Analysis','http://esi.ctv.ca/datafeedrss/vhSportEventClips.aspx?leagueId=9&categoryId=3&binId=1175',97,thumb)
            main.addDir('Samsung Passion Play','http://esi.ctv.ca/datafeedrss/vhBinData.aspx?bid=15421',97,thumb)

        elif murl=='nba':
            main.addDir('Latest','http://esi.ctv.ca/datafeedrss/vhBinData.aspx?bid=1176',97,thumb)
            main.addDir('Highlights','http://esi.ctv.ca/datafeedrss/vhSportEventClips.aspx?leagueId=14&categoryId=1&binId=1176',97,thumb)
            main.addDir('News & Analysis','http://esi.ctv.ca/datafeedrss/vhSportEventClips.aspx?leagueId=14&categoryId=3&binId=1176',97,thumb)
            main.addLink('TEAM CHANNELS','','')
            main.addDir('Raptors','http://esi.ctv.ca/datafeedrss/vhSportEventClips.aspx?teamId=153&binId=1176',97,'http://images.tsn.ca/images/v3/logos/24x24/nba-raptors.png')

        elif murl=='canadian_hockey':
            main.addDir('Latest','http://esi.ctv.ca/datafeedrss/vhBinData.aspx?bid=1174',97,thumb)
            main.addDir('WJC Highlights','http://esi.ctv.ca/datafeedrss/vhSportEventClips.aspx?leagueId=45&categoryId=1&binId=1174',97,thumb)
            main.addDir('WJC News & Analysis','http://esi.ctv.ca/datafeedrss/vhSportEventClips.aspx?leagueId=45&categoryId=3&binId=1174',97,thumb)
            main.addDir('WJC Features','http://esi.ctv.ca/datafeedrss/vhSportEventClips.aspx?leagueId=45&categoryId=4&binId=1174',97,thumb)
            main.addDir("WJC Team Canada Skills",'http://esi.ctv.ca/datafeedrss/vhBinData.aspx?bid=16130',97,thumb)
            main.addDir('Games On-Demand','http://esi.ctv.ca/datafeedrss/vhBinData.aspx?bid=2685',97,thumb)

        elif murl=='cfl':
            main.addDir('Latest','http://esi.ctv.ca/datafeedrss/vhBinData.aspx?bid=1518',97,thumb)
            main.addDir('Highlights','http://esi.ctv.ca/datafeedrss/vhSportEventClips.aspx?leagueId=8&categoryId=1&binId=1518',97,thumb)
            main.addDir('News & Analysis','http://esi.ctv.ca/datafeedrss/vhSportEventClips.aspx?leagueId=8&categoryId=3&binId=1518',97,thumb)
            main.addDir('Games On-Demand','http://esi.ctv.ca/datafeedrss/vhBinData.aspx?bid=1105',97,thumb)
            main.addDir("Grey Cup 100",'http://esi.ctv.ca/datafeedrss/vhBinData.aspx?bid=15576',97,thumb)

        elif murl=='mlb':
            main.addDir('Latest','http://esi.ctv.ca/datafeedrss/vhBinData.aspx?bid=1177',97,thumb)
            main.addDir('News & Analysis','http://esi.ctv.ca/datafeedrss/vhSportEventClips.aspx?leagueId=11&categoryId=3&binId=1177',97,thumb)
            main.addLink('TEAM CHANNELS','','')
            main.addDir('Blue Jays','http://esi.ctv.ca/datafeedrss/vhSportEventClips.aspx?teamId=124&binId=1177',97,'http://images.tsn.ca/images/v3/logos/24x24/mlb-bluejays.png')

        elif murl=='soccer':
            main.addDir('Latest','http://esi.ctv.ca/datafeedrss/vhBinData.aspx?bid=7481',97,thumb)
            main.addDir('MLS','http://esi.ctv.ca/datafeedrss/vhSportEventClips.aspx?leagueId=15&binId=7481',97,thumb)
            main.addDir('Premier League','http://esi.ctv.ca/datafeedrss/vhSportEventClips.aspx?leagueId=16&binId=7481',97,thumb)

        elif murl=='shows':
            main.addDir('Off The Record','http://esi.ctv.ca/datafeedrss/vhBinData.aspx?bid=1100',97,thumb)
            main.addDir('The Reporters','http://esi.ctv.ca/datafeedrss/vhBinData.aspx?bid=1101',97,thumb)
            main.addDir('SC Top 10','http://esi.ctv.ca/datafeedrss/vhBinData.aspx?bid=8884',97,thumb)
            main.addDir("That's Hockey",'http://esi.ctv.ca/datafeedrss/vhBinData.aspx?bid=2452',97,thumb)
            main.addDir("TH2N",'http://esi.ctv.ca/datafeedrss/vhBinData.aspx?bid=9598',97,thumb)
            main.addDir('Cabbie Presents','http://esi.ctv.ca/datafeedrss/vhBinData.aspx?bid=10907',97,thumb)

def TSNLIST(murl):
        main.GA("TSN","TSN-list")
        murl=murl+'&pageSize=200'
        link=main.OPENURL(murl)
        match = re.compile('<id>(.+?)</id>.+?<title><(.+?)></title><description><(.+?)></description><imgUrl>(.+?)</imgUrl>').findall(link)
        for url,name,desc,thumb in match:
            name=name.replace('![CDATA[','').replace(']]','').replace('/',' ')
            desc=desc.replace('![CDATA[','').replace(']]','').replace('/',' ')
            main.addPlayMs(name,url,98,thumb,desc,'','','','')

def TSNLINK(mname,murl,thumb):
        #got help from TSN plugin by TEEFER
        main.GA("TSN-list","Watched")
        ok=True
        url = 'http://esi.ctv.ca/datafeed/urlgenjs.aspx?vid=' + murl
        link=main.OPENURL(url)
        rtmpe = re.compile("Video.Load.+?{url:'(.+?)'").findall(link)
        parsed = urlparse.urlparse(rtmpe[0])
        match = re.compile("country_blocked").findall(rtmpe[0])
        if len(match)>0:
                xbmc.executebuiltin("XBMC.Notification(Sorry!,Playable Only in Canada,5000)")
        else:
            if parsed.netloc == 'tsn.fcod.llnwd.net':
                rtmp = 'rtmpe://tsn.fcod.llnwd.net/a5504'
                auth = re.compile('a5504/(.+?)\'').findall(link)
                playpath = re.compile('ondemand/(.+?).mp4').findall(rtmpe[0])
                stream_url = rtmp + ' playpath=mp4:' + auth[0]
            elif parsed.netloc == 'ctvmms.rd.llnwd.net':
                rtmp = 'http://ctvmms.vo.llnwd.net/kip0/_pxn=1+_pxI0=Ripod-h264+_pxL0=undefined+_pxM0=+_pxK=19321+_pxE=mp4/'
                pathmp4 = re.compile('ctvmms.rd.llnwd.net/(.+?).mp4').findall(rtmpe[0])
                stream_url = rtmp + pathmp4[0] + '.mp4'
            elif parsed.netloc == 'tsnpmd.akamaihd.edgesuite.net':
                match = re.compile('(.+?)_0.?.mp4').findall(rtmpe[0])
                if selfAddon.getSetting("tsn-qua") == "0":
                        stream_url = match[0]+'_05.mp4'
                elif selfAddon.getSetting("tsn-qua") == "1":
                        stream_url = match[0]+'_04.mp4'
                elif selfAddon.getSetting("tsn-qua") == "2":
                        stream_url = match[0]+'_01.mp4'
        
            else:
                rtmp = re.compile('rtmpe(.+?)ondemand/').findall(rtmpe[0])
                rtmp = 'rtmpe' + rtmp[0] + 'ondemand?'
                auth = re.compile('\?(.+?)\'').findall(link)
                path = re.compile('ondemand/(.+?)Adaptive_.+?.mp4\?').findall(rtmpe[0])
                if len(path)==0:
                    path = re.compile('ondemand/(.+?)\?').findall(rtmpe[0])
                    playpath = ' playpath=mp4:' + path[0]
                    stream_url = rtmp + auth[0] + playpath   
                else:
                    playpath = ' playpath=mp4:' + path[0]
                    if selfAddon.getSetting("tsn-qua") == "0":
                        stream_url = rtmp + auth[0] + playpath+'Adaptive_05.mp4'
                    elif selfAddon.getSetting("tsn-qua") == "1":
                        stream_url = rtmp + auth[0] + playpath+'Adaptive_03.mp4'
                    elif selfAddon.getSetting("tsn-qua") == "2":
                        stream_url = rtmp + auth[0] + playpath+'Adaptive_01.mp4'

            # play with bookmark
            player = playbackengine.PlayWithoutQueueSupport(resolved_url=stream_url, addon_id=addon_id, video_type='', title=mname,season='', episode='', year='',img=thumb,infolabels='', watchedCallbackwithParams=main.WatchedCallbackwithParams,imdb_id='')
            #WatchHistory
            if selfAddon.getSetting("whistory") == "true":
                    wh.add_item(mname+' '+'[COLOR green]TSN[/COLOR]', sys.argv[0]+sys.argv[2], infolabels='', img=thumb, fanart='', is_folder=False)
            player.KeepAlive()
            return ok

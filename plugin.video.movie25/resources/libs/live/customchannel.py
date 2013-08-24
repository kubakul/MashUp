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
xmlPath = selfAddon.getSetting('xml-folder')

def MAIN():
    main.addPlayc('My XML Channel Instructions','nills',248,art+'/xml.png','','','','','')
            
    if os.path.exists(xmlPath):
        xmlfolder=os.path.join(xmlPath,'MyXmlChannels')        
        try:
            os.makedirs(xmlfolder)
            xbmc.executebuiltin("XBMC.Notification(Attention!,MyXmlChannel Folder Created,5000,"")")
        except:
            pass
        for path, subdirs, files in os.walk(xmlfolder):
            for filename in files:
                if re.findall('.xml',filename):
                    name =filename.replace('.xml','')
                    url=xmlfolder+'/'+filename
                    thumbfile=os.path.join(xmlfolder,name+'.png')
                    if not os.path.exists(thumbfile):
                        thumbfile=os.path.join(xmlfolder,name+'.jpg')
                    fanfile=os.path.join(xmlfolder,name+'Fanart.png')
                    if not os.path.exists(fanfile):
                        fanfile=os.path.join(xmlfolder,name+'Fanart.jpg')
                    if os.path.exists(thumbfile):
                        if 'png' in thumbfile:
                            thumb=xmlfolder+'/'+name+'.png'
                        else:
                            thumb=xmlfolder+'/'+name+'.jpg'
                    else:
                        thumb=''
                    if os.path.exists(fanfile):
                        if 'png' in fanfile:
                            fan=xmlfolder+'/'+name+'Fanart.png'
                        else:
                            fan=xmlfolder+'/'+name+'Fanart.jpg'
                    else:
                        fan=''
            
                    main.addDirc(name,url,239,thumb,'',fan,'','','')
    else:
        dialog = xbmcgui.Dialog()
        dialog.ok("MashUp", "Please set Custom Xml file Path", "in Addon settings under Custom Channels tab")
        selfAddon.openSettings()

def XmlIns():
        dir = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.movie25/resources/message', ''))
        chlg = os.path.join(dir, 'xmlchannels.txt')
        main.TextBoxes("[B][COLOR red]MashUp XML Instructions![/B][/COLOR]",chlg)
        
def LIST(mname,murl):
    items=[]
    i=0
    f = open(murl)
    text = f.read()
    name=re.findall('<title>([^<]+)</title>',text)
    for names in name:
        name=re.findall('<title>([^<]+)</title>',text)
        url=re.findall('<link>([^<]+)</link>',text)
        thumb=re.findall('<thumbnail>([^<]+)</thumbnail>',text)
        items.append({
            'title': name[i],
            'thumbnail': thumb[i],
            'path': url[i]
        })
        print name[i]
        i=i+1
    for channels in items:
        main.addPlayL(channels['title'],channels['path'],240,channels['thumbnail'],'','','','','')
    
def LINK(mname,murl,thumb):
        main.GA(mname,"Watched")
        ok=True
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        stream_url = murl
        listitem = xbmcgui.ListItem(thumbnailImage=thumb)
        listitem.setInfo('video', {'Title': mname, 'Genre': 'Custom'} )
        playlist.add(stream_url,listitem)
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(playlist)
        #WatchHistory
        if selfAddon.getSetting("whistory") == "true":
            wh.add_item(mname+' '+'[COLOR green]Custom Channel[/COLOR]', sys.argv[0]+sys.argv[2], infolabels='', img=thumb, fanart='', is_folder=False)
        return ok    

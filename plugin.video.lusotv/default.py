# -*- coding: utf-8 -*-
# By AddonBrasil - 23/07/2015
###############################################################################

import xbmc,xbmcaddon,xbmcgui,xbmcplugin,urllib,urllib2,os,re,sys,datetime,time

###############################################################################

from resources.lib.UniversalAnalytics import Tracker

addon_id    = 'plugin.video.lusotv'
selfAddon   = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
icon        = addonfolder + '/icon.png'
fanart      = addonfolder + '/fanart.jpg'
base        = 'http://lusotv.addonbrasil.tk/'

ga = {
	"enabled"    : True,
	"UA"         : 'UA-67989726-1',
	"appName"    : selfAddon.getAddonInfo("name"),
	"appVersion" : selfAddon.getAddonInfo("version"),
	"appId"      : selfAddon.getAddonInfo("id")
}

tracker = Tracker.create(ga["UA"]);
tracker.set("appName", ga["appName"]);
tracker.set("appVersion", ga["appVersion"]);
tracker.set("appId", ga["appId"]);

#ga["enabled"] = True;

if (selfAddon.getSetting("uuid") == ""):
	selfAddon.setSetting("uuid", tracker.params["cid"]);
else:
	tracker.set("clientId", selfAddon.getSetting("uuid"));

###############################################################################

def menuPrincipal(url):
		tracker.send("screenview", screenName="Menu Principal")

		getMenu(url)
		
def getMenu(url):
		tracker.send("screenview", screenName="Get Menu")

		linhas = urllib2.urlopen(url).readlines()
		totLines = len(linhas)
		
		for linha in linhas :
				linha = linha.replace('\n','')
				
				if linha[:1] != '#' :
						params = linha.split(' | ')
						
						if params[0] != '' :
								opcao = params[0]
								img   = base + 'imgs/' + params[1] 
								link  = base + params[2].strip()
								sub   = params[3].strip()
								
								if  sub == "S" : addDir(opcao, link, 1, img, totLines)
								else           : addDir(opcao, link, 10, img, totLines)
								
		xbmcplugin.setContent(int(sys.argv[1]), 'movies')
		xbmc.executebuiltin("Container.SetViewMode(500)")
		
def getCanais(url, name):
		tracker.send("screenview", screenName="Get Canais - "+ name)

		linhas = urllib2.urlopen(url).readlines()
		totLinhas = len(linhas)

		for linha in linhas :
				linha = linha.replace('\r\n','')
				
				if linha[:1] != '#' :
						params = linha.split(' | ')
						
						if params[0] != '' :
								nome  = params[0]
								img   = base + 'imgs/' + params[1] 
								links = params[2].replace(' rtmp','rtmp').replace(' rtsp','rtsp').replace(' http','http').rstrip()
								
								addDir(nome, links, 100, img, totLinhas, False)
							
		xbmcplugin.setContent(int(sys.argv[1]), 'movies')
		xbmc.executebuiltin("Container.SetViewMode(500)")

		
###############################################################################

def addDir(name, url, mode, iconimage, total=0, pasta=True ,fanart=fanart):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)
    liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name})
    contextMenuItems = []
    contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
    liz.addContextMenuItems(contextMenuItems, replaceItems=True)
    liz.setProperty('fanart_image', fanart)
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=pasta, totalItems=total)
			
def doPlay(url, name, iconimage):
		links = url.split(',')
		
		tracker.send("event", "Usage", "Play Video - " + name, "episode", screenName="Play Screen");
		
		playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
		playlist.clear()
		
		try:
				for link in links:
						listitem = xbmcgui.ListItem(name, thumbnailImage=iconimage)
						listitem.setInfo('video', {'Title': name})
						playlist.add(url=link, listitem=listitem, index=7)
						
				xbmc.Player(xbmc.PLAYER_CORE_AUTO).play(playlist)
		except:
				pass
				
###############################################################################

def get_params():
      param=[]
      paramstring=sys.argv[2]
      if len(paramstring)>=2:
            params=sys.argv[2]
            cleanedparams=params.replace('?','')
            if (params[len(params)-1]=='/'):
                  params=params[0:len(params)-2]
            pairsofparams=cleanedparams.split('&')
            param={}
            for i in range(len(pairsofparams)):
                  splitparams={}
                  splitparams=pairsofparams[i].split('=')
                  if (len(splitparams))==2:
                        param[splitparams[0]]=splitparams[1]                 
      return param

params=get_params()
url       = None
name      = None
iconimage = None
mode      = None

try    : url = urllib.unquote_plus(params["url"])
except : pass
try    : iconimage = urllib.unquote_plus(params["iconimage"])
except : pass
try    : name = urllib.unquote_plus(params["name"])
except : pass
try    : mode = int(params["mode"])
except : pass

###############################################################################

#print "Mode : " + str(mode)
#print "Icon : " + str(iconimage)
#print "URL  : " + str(url)
#print "Name : " + str(name)

if  mode == None : 
		try : 
				Tracker
		except NameError:
				from UniversalAnalytics import Tracker;
				tracker = Tracker.create(ga["UA"]);
				tracker.set("appName", ga["appName"]);
				tracker.set("appVersion", ga["appVersion"]);
				tracker.set("appId", ga["appId"]);
				
				if (selfAddon.getSetting("uuid") == ""):
					selfAddon.setSetting("uuid", tracker.params["cid"]);
				else:
					tracker.set("clientId", selfAddon.getSetting("uuid"));
			
		tracker.send("event", "Usage", "install", screenName="Menu Principal")

		menuPrincipal(url=base+'?a=menu.ltv')
elif mode == 1    : getMenu(url, name)
elif mode == 10   : getCanais(url, name)
elif mode == 100  : doPlay(url, name, iconimage)

xbmcplugin.endOfDirectory(int(sys.argv[1]))

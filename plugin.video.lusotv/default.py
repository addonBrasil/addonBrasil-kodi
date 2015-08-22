# -*- coding: utf-8 -*-
# By AddonBrasil
###############################################################################

import xbmc,xbmcaddon,xbmcgui,xbmcplugin,urllib,urllib2,os,re,sys,datetime,time

###############################################################################
versao = '1.0.1'
addon_id = 'plugin.video.lusotv'
selfAddon = xbmcaddon.Addon(id=addon_id)
base = 'http://lusotv.addonbrasil.tk'
art  = base + '/imgs/'

###############################################################################

def menuPrincipal():
		addDir('Generalistas'   , base, 10, art + 'general.png'   , 1)
		addDir('Desportos'      , base, 10, art + 'desporto.png'  , 2)
		addDir('Notícias'       , base, 10, art + 'noticias.png'  , 3)
		addDir('Religiosos'     , base, 10, art + 'religiosos.png', 4)
		addDir('Filmes & Séries', base, 10, art + 'filmseries.png', 5)
		
		xbmc.executebuiltin("Container.SetViewMode(50)")

def getCanais(url, group):
		for line in urllib2.urlopen(url).readlines():
				params = line.split(' | ')
				
				if str(group) == str(params[0]) :
						nome = params[1]
						img = art + params[2] 
						links = params[3].replace(' rtmp','rtmp').replace(' rtsp','rtsp').replace(' http','http').rstrip()
						addDir2(nome, links, 100, img)
							
		xbmc.executebuiltin("Container.SetViewMode(500)")

###############################################################################

def addDir(name, url, mode, iconimage, group, total=0, pasta=True, plot='', fanart=''):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage) + "&group=" + str(group)
    liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": plot})
    contextMenuItems = []
    contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
    liz.addContextMenuItems(contextMenuItems, replaceItems=True)
    liz.setProperty('fanart_image', fanart)
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=pasta, totalItems=total)
			
def addDir2(name, url, mode, iconimage, total=0, pasta=False, plot='', fanart=''):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)
    liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": plot})
    contextMenuItems = []
    contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
    liz.addContextMenuItems(contextMenuItems, replaceItems=True)
    liz.setProperty('fanart_image', fanart)
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=pasta, totalItems=total)
			
def doPlay(url, name, iconimage):
		links = url.split(',')
		
		playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
		playlist.clear()
		
		try:
				for link in links:
						print link
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
group     = None
mode      = None
tamanhoparavariavel=None

try    : url = urllib.unquote_plus(params["url"])
except : pass
try    : tamanhoparavariavel = urllib.unquote_plus(params["tamanhof"])
except : pass
try    : iconimage = urllib.unquote_plus(params["iconimage"])
except : pass
try    : group = int(params["group"])
except : pass
try    : name = urllib.unquote_plus(params["name"])
except : pass
try    : mode = int(params["mode"])
except : pass

###############################################################################

#print "Mode : " + str(mode)
#print "Icon : " + str(iconimage)
#print "Group: " + str(group)
#print "URL  : " + str(url)
#print "Name : " + str(name)
#print "Var  : " + str(tamanhoparavariavel)

if mode   == None : menuPrincipal()
elif mode == 10   : getCanais(url, group)
elif mode == 100  : doPlay(url, name, iconimage)

xbmcplugin.endOfDirectory(int(sys.argv[1]))

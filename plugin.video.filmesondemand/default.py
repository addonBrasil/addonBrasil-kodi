# -*- coding: utf-8 -*-
#
# 21/08/2015 - By AddonBrasil
###############################################################################

import xbmc,xbmcaddon,xbmcgui,xbmcplugin,urllib,urllib2,os,re,sys,datetime,time

from t0mm0.common.addon import Addon
from metahandler import metahandlers

###############################################################################

versao = '1.0.0'
addon_id = 'plugin.video.filmesondemand'
selfAddon = xbmcaddon.Addon(id=addon_id)
metaget = metahandlers.MetaData(preparezip=False)
datapath= xbmc.translatePath(selfAddon.getAddonInfo('profile'))
addon = Addon(addon_id, sys.argv)
addonfolder = selfAddon.getAddonInfo('path')
icon   = addonfolder + '/icon.png'
fanart = addonfolder + '/fanart.jpg'
artfolder = addonfolder + '/resources/art/'

metaset = selfAddon.getSetting('enable_meta')

base = 'http://fod.addonbrasil.tk'

###############################################################################

def menuPrincipal():
		addDir2('LISTA'     , base, 10, artfolder + 'lista.png')
		addDir2('DUBLADOS'  , base, 10, artfolder + 'dublados.png')
		addDir2('LEGENDADOS', base, 22, artfolder + 'legendados.png')
		
def menuLetras(url, name):
		if name == "LISTA"      : modo = 20
		if name == "DUBLADOS"   : modo = 21
		#if name == "LEGENDADOS" : modo = 22

		addDir2('A', url, modo, artfolder + 'a.png')
		addDir2('B', url, modo, artfolder + 'b.png')
		addDir2('C', url, modo, artfolder + 'c.png')
		addDir2('D', url, modo, artfolder + 'd.png')
		addDir2('E', url, modo, artfolder + 'e.png')
		addDir2('F', url, modo, artfolder + 'f.png')
		addDir2('G', url, modo, artfolder + 'g.png')
		addDir2('H', url, modo, artfolder + 'h.png')
		addDir2('I', url, modo, artfolder + 'i.png')
		addDir2('J', url, modo, artfolder + 'j.png')
		addDir2('K', url, modo, artfolder + 'k.png')
		addDir2('L', url, modo, artfolder + 'l.png')
		addDir2('M', url, modo, artfolder + 'm.png')
		addDir2('N', url, modo, artfolder + 'n.png')
		addDir2('O', url, modo, artfolder + 'o.png')
		addDir2('P', url, modo, artfolder + 'p.png')
		addDir2('Q', url, modo, artfolder + 'q.png')
		addDir2('R', url, modo, artfolder + 'r.png')
		addDir2('S', url, modo, artfolder + 's.png')
		addDir2('T', url, modo, artfolder + 't.png')
		addDir2('U', url, modo, artfolder + 'u.png')
		addDir2('V', url, modo, artfolder + 'v.png')
		addDir2('W', url, modo, artfolder + 'w.png')
		addDir2('X', url, modo, artfolder + 'x.png')
		addDir2('Y', url, modo, artfolder + 'y.png')
		addDir2('Z', url, modo, artfolder + 'z.png')
		
		xbmc.executebuiltin("Container.SetViewMode(500)")

def getFilmes(url, name):
		for line in urllib2.urlopen(url).readlines():
				params = line.split(' | ')
				
				titulo = params[0].encode('utf-8', 'ignore').replace('-', ' ').replace(' LEG',' (Legendado)')
				link   = params[1].replace(' http', 'http')
				
				
				if mode == 22 :
						if '(Legendado)' in titulo: 
								#if titulo[:1] == name :
								addDir(titulo, link, 100, '',1,False)
				elif mode == 21:
						if not '(Legendado)' in titulo: 
								if titulo[:1] == name :
									addDir(titulo, link, 100, '',1,False)
				else:
						if titulo[:1] == name :
							addDir(titulo, link, 100, '',1,False)

		if metaset=='true':
				setView('movies', 'MAIN')
		else: 
				xbmc.executebuiltin("Container.SetViewMode(50)")

def addDir(name,url,mode,iconimage,itemcount=1,isFolder=True):
		if metaset=='true':
				if '(Legendado)' in name: 
						splitName  = name.partition('(Legendado)')
						simpleName = splitName[0]
				else :
						splitName  = name
						simpleName = splitName
						
				meta = metaget.get_meta('movie', simpleName ,'')
				u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&site="+str(site)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
				ok=True
				
				liz=xbmcgui.ListItem(name, iconImage=meta['cover_url'], thumbnailImage=meta['cover_url'])
				
				liz.setInfo(type="Video", infoLabels= meta)
				
				contextMenuItems = []
				contextMenuItems.append(('Informações do Filme', 'XBMC.Action(Info)'))
				
				liz.addContextMenuItems(contextMenuItems, replaceItems=False)
				
				if not meta['backdrop_url'] == '': 
						liz.setProperty('fanart_image', meta['backdrop_url'])
				else: 
						liz.setProperty('fanart_image', fanart)
						
				ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder,totalItems=itemcount)
				
				return ok
		else:
				u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&site="+str(site)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
				ok=True
				liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
				liz.setInfo( type="Video", infoLabels={ "Title": name } )
				liz.setProperty('fanart_image', fanart)
				ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder)
				return ok

def addDir2(name,url,mode,iconimage):
        xbmc.executebuiltin('Container.SetViewMode(50)')
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
				
def doPlay(url, name, iconimage):
		links = url.split(',')
		
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
				
def setView(content, viewType):
    if content : xbmcplugin.setContent(int(sys.argv[1]), content)
    if selfAddon.getSetting('auto-view')=='true' : xbmc.executebuiltin("Container.SetViewMode(%s)" % selfAddon.getSetting(viewType) )

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

params    = get_params()
site      = None
url       = None
name      = None
iconimage = None
group     = None
mode      = None

try    : url = urllib.unquote_plus(params["site"])
except : pass
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
#print "Site : " + str(site)
#print "URL  : " + str(url)
#print "Name : " + str(name)

if mode == None or url == None or len(url) < 1            : menuPrincipal()
elif mode == 10                                           : menuLetras(url, name)
elif mode == 20 or mode == 21 or mode == 22 or mode == 30 : getFilmes(url, name)
elif mode == 100                                          : doPlay(url, name, iconimage)

xbmcplugin.endOfDirectory(int(sys.argv[1]))

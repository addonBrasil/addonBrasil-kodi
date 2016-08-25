#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# By AddonBrasil - 25/08/16
#########################################################################

import urllib, urllib2, re, xbmcplugin, xbmcgui, xbmc, xbmcaddon, HTMLParser, sys

from BeautifulSoup import BeautifulSoup

addon_id    = 'plugin.video.cartoons'
selfAddon   = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder   = addonfolder + '/resources/img/'
icon        = addonfolder + '/icon.png'
fanart      = addonfolder + '/fanart.jpg'
base        = 'http://www.animeai.net/223615.html'

def menuPrincipal(url):
		link = openURL(url)
		link = unicode(link, 'latin-1', errors='ignore')
		
		soup = BeautifulSoup(link)
		cont  = soup.findAll("div", { "id" : "listaDesenhos" })
		lista = cont[0]("li")
		
		totD = len(lista)
		
		for item in lista:
				urlD = item.a["href"]
				
				if len(urlD) > 3 :
						titD = item.text.replace('&#8211;','-').encode('iso-8859-1')

						addDir(titD, urlD, 10, icon, True, totD, '')
				
def getEpisodios(name,url, iconimage):
		link = openURL(url)
		link = unicode(link, 'latin-1', errors='ignore')
		soup = BeautifulSoup(link)
		conteudo  = soup.findAll("div", { "class" : "contentBox" })
		eps = conteudo[0]("li")
		
		totE = len(eps)
		
		for ep in eps:
				titE = ep.a.text.replace('&#8211;','-').encode('iso-8859-1')
				
				if not 'Todos os' in titE :
						urlE = ep.a["href"]
						imgE = re.findall("<meta property='og:image' content='(.*?)'.*?>", link)[0]
						imgE = imgE.encode('iso-8859-1')

						addDir(titE, urlE, 100, imgE, False, totE, '')
						
def doPlay(url, name, iconimage):
		link = openURL(url)
		
		url2Play = re.findall('<video src="(.*?)" width=', link)[0]
		
		if not url2Play : return
		
		playlist = xbmc.PlayList(1)
		
		playlist.clear()
		
		listitem = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
		listitem.setInfo("Video", {"Title":name})
		listitem.setProperty('mimetype', 'video/mp4')
		listitem.setProperty('IsPlayable', 'true')

		playlist.add(url2Play,listitem)
		xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
		xbmcPlayer.play(playlist)

###################################################################################

def addDir(name,url,mode,iconimage,pasta=True,total=1,plot=''):
		u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
		ok=True
		liz=xbmcgui.ListItem(name, iconImage="iconimage", thumbnailImage=iconimage)
		liz.setProperty('fanart_image', iconimage)
		liz.setInfo( type="video", infoLabels={ "title": name, "plot": plot } )
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
		return ok

def addDir2(name,url,mode,iconimage,pasta=True,total=1,plot=''):
		u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
		ok=True
		liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
		liz.setProperty('fanart_image', fanart)
		liz.setInfo( type="video", infoLabels={ "title": name, "plot": plot } )
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
		return ok
	
def openURL(url):
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		return link

###################################################################################

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
url       = None
name      = None
mode      = None
iconimage = None

try    : url=urllib.unquote_plus(params["url"])
except : pass

try    : name=urllib.unquote_plus(params["name"])
except : pass

try    : mode=int(params["mode"])
except : pass

try    : iconimage=urllib.unquote_plus(params["iconimage"])
except : pass

if   mode == None : menuPrincipal(url=base)
elif mode == 10   :	getEpisodios(name, url, iconimage)
elif mode == 100  :	doPlay(url, name, iconimage)
	
xbmcplugin.endOfDirectory(int(sys.argv[1]))
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# By AddonBrasil - 28/07/2015
#####################################################################

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,HTMLParser,os
import httplib

from urlparse      import urlparse
from BeautifulSoup import BeautifulSoup

h = HTMLParser.HTMLParser()

versao      = '1.1.0'
addon_id    = 'plugin.video.arquivobrasil'
selfAddon   = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')

icon      = addonfolder + '/icon.png'
fanart    = addonfolder + '/fanart.jpg'
artfolder = addonfolder + '/resources/art/'

base = 'http://novelasgravadas.net/'

#####################################################################

def menuPrincipal():
		addDir('Novelas'   , base, 10, artfolder + 'novelas.jpg')
		addDir('Séries'    , base, 10, artfolder + 'series.jpg')
		addDir('Jornalismo', base, 10, artfolder + 'jornalismo.jpg')
		addDir('Variedades', base, 10, artfolder + 'variedades.jpg')
		addDir('Esportes'  , base, 10, artfolder + 'esportes.jpg')

		xbmc.executebuiltin('Container.SetViewMode(50)')
		
def getListaCat(url, name):
		link = openURL(url)
		soup = BeautifulSoup(link)
		conteudo = soup("div", {"id": "navigation"})
		
		listaGeral = conteudo[0]("ul", {"class": "sub-menu"} )
		
		if name   == 'Novelas'    : temp = listaGeral[0]
		elif name == 'Séries'     : temp = listaGeral[1]
		elif name == 'Jornalismo' : temp = listaGeral[2]
		elif name == 'Variedades' : temp = listaGeral[3]
		elif name == 'Esportes'   : temp = listaGeral[4]
		
		categorias = temp("li")
		
		totCategorias = len(categorias)
		
		for categoria in categorias:
				titcat = categoria.text.replace('&#038;','&').encode('utf-8', 'ignore')
				urlcat = categoria.a["href"]
				imgcat = artfolder + getImg(titcat) + '.png'
				addDir(titcat, urlcat, 20, imgcat, totCategorias, True)				

		xbmc.executebuiltin('Container.SetViewMode(500)')
		
def getVideosCat(url, name, iconimage):
		link  = openURL(url)
		soup  = BeautifulSoup(link)
		
		conteudo = soup("div", {"class": "block archive"})
		videos   = conteudo[0]("div", {"class": "block-image"})
		
		totVideos = len(videos)
		
		for video in videos:
				url = video.a["href"]
				tit = video.img["alt"].replace('&#038;','&').replace('&#8211;',"-").replace(' de ',' - ').replace(' Completo','').encode('utf-8', 'ignore')
				img = video.img["src"] 
				addDir(tit, url, 100, img, False, totVideos)
				
		try :
				page = re.compile("<span class='current'>.+?</span><a href='(.+?)' class='inactive' >.+?</a>").findall(link)
				
				for prox_pagina in page:
						addDir('Página Seguinte >>',prox_pagina,20,artfolder + 'prox.jpg')
						break
		except :
				pass
				
		xbmc.executebuiltin('Container.SetViewMode(50)')

def doPlay(url, name):
		link = openURL(url)

		pg = 0
		msgDialog = xbmcgui.DialogProgress()

		msgDialog.create('ARQUIVO BRASIL', 'Abrindo Sinal', name, 'Por favor aguarde...')
		msgDialog.update(25)
		
		playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
		playlist.clear()

		msgDialog.update(50)
		
		try :
				url2Rslv = re.findall('<IFRAME SRC="(.*?)" FRAMEBORDER=0 MARGINWIDTH=0 MARGINHEIGHT=0 SCROLLING=NO WIDTH=645 HEIGHT=355></IFRAME>', link)[0]
				url2Play = getURL2Play(url2Rslv)
		except:
				url2Rslv = re.findall('flashvars="&#038;file=(.*?)&#038;skin', link)[0]
				linkRslv = openURL(url2Rslv)
				url2Play = re.findall('<location>(.*?)</location>', linkRslv)[0]
		
		msgDialog.update(75)
		
		if url2Play:
				liz = xbmcgui.ListItem(name, thumbnailImage=iconimage)
				liz.setInfo('video', {'Title': name})
				liz.setPath(url)
				liz.setProperty('mimetype','video/mp4')
				liz.setProperty('IsPlayable', 'true')
				
				playlist.add(url=url2Play, listitem=liz, index=7)
						
				msgDialog.update(100)
				xbmc.Player(xbmc.PLAYER_CORE_AUTO).play(playlist)
		else:
				msgDialog.update(100)
				dialog = xbmcgui.Dialog()
				dialog.ok("ARQUIVO BRASIL", "Video Indisponível", "Este video ainda não esta disponível...", "Tente novamente em breve.")		

def openURL(url):
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = urllib2.urlopen(req)
		link = response.read()
		response.close()
		
		return link
		
def addLink(name,url,iconimage):
		ok = True
		liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
		liz.setProperty('fanart_image', fanart)
		liz.setInfo( type="Video", infoLabels={ "Title": name } )
		ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
		
		return ok

def addDir(name, url, mode, iconimage, pasta=True, total=1, plot=''):
		u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
		ok = True
		liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
		liz.setProperty('fanart_image', fanart)
		liz.setInfo( type="video", infoLabels={ "title": name, "plot": plot } )
		ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=pasta, totalItems=total)

		return ok
		
def getURL2Play(url):
		link = openURL(url)

		try:
				urlFile  = re.findall(r'file: "(.*?).m3u8',link)[0]
				urlVideo = urlFile + '.m3u8?embed='
		except:
				urlVideo = '-'
			
		return urlVideo			

def getImg(texto):
		texto = texto.lower()
		texto = texto.replace('ç','c').replace('ã','a').replace('õ','o')
		texto = texto.replace('â','a').replace('ê','e').replace('ô','o')
		texto = texto.replace('á','a').replace('é','e').replace('í','i').replace('Í','i').replace('ó','o').replace('ú','u')
		texto = texto.replace('&','').replace(' ', '-').replace('.', '-').replace(',', '-').replace('--','-')
		
		return texto
		
#####################################################################

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

try    : url = urllib.unquote_plus(params["url"])
except : pass

try    : name = urllib.unquote_plus(params["name"])
except : pass

try    : iconimage=urllib.unquote_plus(params["iconimage"])
except : pass

try    : mode = int(params["mode"])
except : pass

#####################################################################

if   mode == None : menuPrincipal()
elif mode == 10   : getListaCat(url, name)
elif mode == 20   : getVideosCat(url,name, iconimage)
elif mode == 100  : doPlay(url, name)
	
xbmcplugin.endOfDirectory(int(sys.argv[1]))
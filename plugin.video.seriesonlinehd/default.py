#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# By AddonBrasil - 26/08/15
# Atualização 1.0.1: 29/12/2015
# Atualização 1.0.2: 08/04/2016
#############################################################################################

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,HTMLParser,os
import urlresolver
import jsunpack

from bs4 import BeautifulSoup

h = HTMLParser.HTMLParser()

addon_id  = 'plugin.video.seriesonlinehd'
selfAddon = xbmcaddon.Addon(id=addon_id)

addonfolder = selfAddon.getAddonInfo('path')
icon        = addonfolder + '/icon.png'
fanart      = addonfolder + '/fanart.jpg'
artfolder   = addonfolder + '/resources/art/'

base = 'http://www.seriesonlinehd.org'

#############################################################################################

def menuPrincipal():
		addDir2('Séries'      , base, 10, artfolder + 'series.jpg',fanart)
		addDir2('Categorias'  , base, 20, artfolder + 'categorias.jpg',fanart)
		addDir2('Pesquisa'    , base, 50, artfolder + 'pesquisa.jpg',fanart)  
		
		xbmcplugin.setContent(int(sys.argv[1]), 'movies')
		xbmc.executebuiltin('Container.SetViewMode(50)')

def getSeries(url):
		link = openURL(url)
		link = unicode(link, 'ascii', 'ignore')
	
		soup     = BeautifulSoup(link)
		conteudo = soup("div", {"class": "items"})
		
		series   = conteudo[0]("div", {"class" : "imagen"})
		
		totSeries = len(series)

		for serie in series:
				url = serie.a["href"]
				tit = serie.img["alt"].replace(' Online', '').replace(' Dublado e Legendado','').replace(' Dublado e legendado','').replace('Assistir ', '').encode('utf-8','ignore')
				img = serie.img["src"] 
				
				addDir(tit, url, 11, str(img), totSeries, True)

		try : 
				proxima = re.findall('<link rel="next" href="(.*?)"', link)[0]
				addDir2('Próxima Página >>', proxima, 10, artfolder + 'proxima.jpg', fanart)
		except : 
				pass
				
				
		xbmcplugin.setContent(int(sys.argv[1]), 'movies')
		xbmc.executebuiltin('Container.SetViewMode(500)')

def getTemporadas(name, url, iconimage):
		link = openURL(url)
		soup = BeautifulSoup(link)
		
		conteudo   = soup("div", {"class": "ep-list"})
		temporadas = conteudo[0]("td", {"class" : "ep-ntp"})
		
		totTemporadas = len(temporadas)
		
		tempant = ''

		for temporada in temporadas:
				titTemporada = temporada.text.encode('utf-8', 'ignore')
				urlTemporada = url
				if  titTemporada != tempant and titTemporada != '//':
						tempant = titTemporada
						addDir2(titTemporada, urlTemporada, 12, iconimage, fanart)

		xbmcplugin.setContent(int(sys.argv[1]), 'movies')
		xbmc.executebuiltin('Container.SetViewMode(500)')

def getEpisodios(name, url, iconimage):
		link = openURL(url)
		soup = BeautifulSoup(link)
		
		conteudo = soup("div", {"class": "ep-list"})
		tempEP   = conteudo[0]("td", {"class": "ep-ntp"})
		episEP   = conteudo[0]("td", {"class": "ep-nep"})
		#titEP   = conteudo[0]("td", {"class": "ep-tit"})
		#resEP   = conteudo[0]("td", {"class": "ep-res"})
		dubEP    = conteudo[0]("td", {"class": "ep-dub"})
		legEP    = conteudo[0]("td", {"class": "ep-leg"})
		
		totEpisodios = len(tempEP)
		
		e = 0
		
		for e in range(totEpisodios):
				seaE = tempEP[e].text.encode('utf-8', 'ignore')
				
				if seaE == name :
						epsE = episEP[e].text.encode('utf-8', 'ignore')
						#titE = titEP[e].text.encode('utf-8', 'ignore')
						#resE = resEP[e].text.encode('utf-8', 'ignore')
						
						try    : dubE = dubEP[e].a['href']
						except : dubE = ''
								
						try    : legE = legEP[e].a['href']
						except : legE = ''
						
						if 'Episódio' in epsE : titEpisodioT =  seaE + ' - ' + epsE 
						else                  : titEpisodioT =  seaE + ' - Episódio ' + epsE 
						
						if dubE != '' : 
								titEpisodio = titEpisodioT + ' - Dublado' #+ ' - ' + resE
								addDir2(titEpisodio, dubE, 100, iconimage, fanart, False)
								
						if legE != '' :
								titEpisodio = titEpisodioT + ' - Legendado' #+ ' - ' + resE
								addDir2(titEpisodio, legE, 100, iconimage, fanart,False)
						
				e += 1
				
		xbmcplugin.setContent(int(sys.argv[1]), 'movies')
		xbmc.executebuiltin('Container.SetViewMode(50)')
				
def getCategorias(url):                  
		link = openURL(url)
		soup = BeautifulSoup(link)
		
		conteudo   = soup("ul", {"class": "sub-menu"})
		categorias = conteudo[1]("li")
		
		totCategorias = len(categorias)
		
		for categoria in categorias:
				titCat = categoria.text.encode('utf-8', 'ignore')
				urlCat = categoria.a['href']
				addDir(titCat, urlCat, 10, icon, totCategorias, True)
						
		xbmcplugin.setContent(int(sys.argv[1]), 'movies')
		xbmc.executebuiltin('Container.SetViewMode(500)')

def doPesquisa():
		busca =''

		teclado = xbmc.Keyboard(busca, 'Pesquisa Séries Online HD')
		teclado.doModal()

		if teclado.isConfirmed():
				busca = teclado.getText().replace(' ','+')
				
				if len(busca) > 1 : 
						url = base + '/?s=' + busca
						getSeries(url)
				else:
						return				
				
def playVideo(name, url, iconimage):
		OK = True		
		
		mensagemprogresso = xbmcgui.DialogProgress()
		mensagemprogresso.create('Séries Online HD', 'Resolvendo Link','Por favor aguarde...')
		mensagemprogresso.update(33)

		linksE = []
		hostsE = []

		link = openURL(url)
		soup  = BeautifulSoup(link)
		conteudo = soup("div", {"class": "bts"})
		links   = conteudo[0]("a")
		
		for link in links:
				titL = link.text
				urlL = link["href"]
				
				if not 'amv.php' in urlL :
					if not 'cz.php' in urlL :
						if not 'thevid' in urlL :
							linksE.append(urlL)
							hostsE.append(titL.upper())
				
		if not hostsE : return
		
		index = xbmcgui.Dialog().select('Selecione uma das fontes suportadas :', hostsE)
		
		if index == -1 : return
		
		mensagemprogresso.update(25,'Resolvendo fonte Para ' + name, 'Por favor aguarde...')
		
		urlV = linksE[index]
		
		if 'ok' in urlV : 
				okID = urlV.split("key=")[1].replace('&leg=','')
				urlV = 'http://ok.ru/videoembed/' + okID
				
		elif 'thevid' in urlV : 
				tvID = urlV.split("thevid=")[1]
				urlV = 'http://thevid.net/e/' + tvID
				
		elif 'vt.php' in urlV :
				vtID = urlV.split("vt=")[1]
				urlV = 'http://vidto.me/embed-' + vtID

		elif 'vdz.php' in urlV :
				vzID = urlV.split("vdz=")[1]
				urlV = 'http://vidzi.tv/embed-' + vzID
				
		elif 'openload' in urlV :
				olID = urlV.split("open=")[1]
				urlV = 'https://openload.co/embed/' + olID
				
		if OK : urlVideo = urlresolver.HostedMediaFile(urlV).resolve()				
				
		mensagemprogresso.update(100)
		mensagemprogresso.close()

		playlist = xbmc.PlayList(1)
		playlist.clear()
		listitem = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
		listitem.setInfo("Video", {"Title":name})
		listitem.setProperty('mimetype', 'video/x-msvideo')
		playlist.add(urlVideo,listitem)
		xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
		xbmcPlayer.play(playlist)

#############################################################################################

def openURL(url):
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		return link
		
def addDir(name, url, mode, iconimage, pasta=True, total=1, plot=''):
		u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
		ok = True
		liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
		liz.setProperty('fanart_image', fanart)
		liz.setInfo( type="video", infoLabels={ "title": name, "plot": plot } )
		ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=pasta, totalItems=total)

		return ok
		
def addDir2(name,url,mode,iconimage,fanart,pasta=True,description=''):
		u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+str(description)
		ok=True
		liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
		liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
		liz.setProperty('fanart_image', fanart)
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta)
		return ok
				
#############################################################################################
		
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

params =get_params()
mode      = None
site      = None
url       = None 
name      = None 
iconimage = None

try    : mode=int(params["mode"])
except : pass
try    : site=urllib.unquote_plus(params["site"])
except : pass
try    : url=urllib.unquote_plus(params["url"])
except : pass
try    : name=urllib.unquote_plus(params["name"])
except : pass
try    : iconimage=urllib.unquote_plus(params["iconimage"])
except : pass

#print "Site : " + str(site) 
#print "Mode : " + str(mode)
#print "URL  : " + str(url)
#print "Name : " + str(name)
#print "Image: " + str(iconimage)

if   mode == None : menuPrincipal()
elif mode == 10   : getSeries(url)
elif mode == 11   : getTemporadas(name, url, iconimage)
elif mode == 12   : getEpisodios(name, url, iconimage)
elif mode == 20   : getCategorias(url)
elif mode == 50   : doPesquisa()
elif mode == 100  : playVideo(name, url, iconimage)

xbmcplugin.endOfDirectory(int(sys.argv[1]))


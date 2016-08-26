#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# By AddonBrasil - 24/08/15
#########################################################################

import urllib, urllib2, re, xbmcplugin, xbmcgui, xbmc, xbmcaddon, HTMLParser, sys

from xbmcgui import ListItem
from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup


addon_id    = 'plugin.video.animebrasil'
selfAddon   = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder   = addonfolder + '/resources/img/'
fanart      = addonfolder + '/fanart.jpg'
base        = 'http://anitube.info'

def menuPrincipal():
		addDir2('Gêneros'    , base + '/genero'            , 10, artfolder + 'categorias.jpg')
		addDir2('Lançamentos', base + '/animes-lancamentos', 20, artfolder + 'recentes.jpg')
		addDir2('Legendados' , base + '/anime'             , 30, artfolder + 'comentados.jpg')
		addDir2('Pesquisa'   , base                        , 99, artfolder + 'pesquisa.jpg')
		
def getGeneros(url):
		link = openURL(url)
		
		soup    = BeautifulSoup(link)
		generos = soup.find("div", { "class" : "row" }).findAll('a')
		totG    = len(generos)

		for genero in generos:
				titG  = genero.text.encode('utf-8', 'ignore')
				urlG  = base + genero["href"]
				imgG  = artfolder + 'categorias.jpg'

				addDir(titG, urlG, 11, imgG, True, totG)
				
def getAnimesGen(url):
		link  = openURL(url)
		link  = unicode(link, 'latin', errors='ignore')
		
		urlsA = re.findall('<h2 class="go"><a class="internalUrl" href="(.*?)" title="(.*?)" rel="bookmark" itemprop="name">', link)
		imgsA = re.findall('<img class="img-responsive" alt=".*?" title=".*?" src="(.*?)" itemprop="image">', link)
		
		totA  = len(imgsA)
		
		for i in range(totA):
				titA = urlsA[i][1].encode('ascII', 'ignore')
				urlA = base + urlsA[i][0]
				imgA = imgsA[i]
				
				addDir(titA, urlA, 31, imgA, True, totA, '')
				
		try :
				proxima = re.findall('href="(.*?)">Avançar</a></li>', link)[0]
				addDir('Próxima Página >>', base + proxima, 30, artfolder + 'proxpag.jpg')
		except :
				pass
		
def getLancamentos(url):
		link = openURL(url)
		
		soup = BeautifulSoup(link)
		episodios = soup.findAll("div", {"class" : "well well-sm"})
		
		
		totE = len(episodios)
		
		for episodio in episodios:
				titE = episodio.a.img["alt"].encode('utf-8', 'ignore')
				urlE = base + episodio.a["href"]
				imgE = episodio.a.img['src']
				addDir(titE, urlE, 100, imgE, False, totE, '')
				
		try :
				pp = re.findall('href="(.*?)">Avançar</a></li>', link)[0]
				addDir('Próxima Página >>', base + proxima, 20, artfolder + 'proxpag.jpg')

		except :
				pass
		
def getLegendados(url):
		link  = openURL(url)
		link  = unicode(link, 'latin', 'ignore')
		urlsA = re.findall('<h2 class="go"><a class="internalUrl" href="(.*?)" title="(.*?)" rel="bookmark" itemprop="name">', link)
		imgsA = re.findall('<img class="img-responsive" alt=".*?" title=".*?" src="(.*?)" itemprop="image">', link)

		totA  = len(imgsA)
		
		for i in range(totA):
				titA = urlsA[i][1].encode('ascii', 'ignore')
				urlA = base + urlsA[i][0]
				imgA = imgsA[i]
				
				addDir(titA, urlA, 31, imgA, True, totA, '')
				
		try :
				proxima = re.findall('href="(.*?)">Avançar</a></li>', link)[0]
				addDir('Próxima Página >>', base + proxima, 30, artfolder + 'proxpag.jpg')
		except :
				pass
		
def getEpsLegendados(url):
		link = openURL(url)
		soup = BeautifulSoup(link, convertEntities=BeautifulSoup.HTML_ENTITIES)
		eps  = soup.findAll("div", { "class" : "well well-sm" })
		
		plotE = re.findall('<span itemprop="description">(.*?)</span>', link, re.DOTALL|re.MULTILINE)[0]
		plotE = unicode(BeautifulStoneSoup(plotE,convertEntities=BeautifulStoneSoup.HTML_ENTITIES )).encode('utf-8')

		totE = len(eps)
		
		for ep in eps:
				try :
						titE = ep.img["title"].encode('ascii', 'ignore')
						urlE = base + ep.a["href"]
						imgE = ep.img['src']
						addDir(titE, urlE, 100, imgE, False, totE, plotE)
				except:
						pass
						
		try :
				proxima = re.findall('href="(.*?)">Avançar</a></li>', link)[0]
				addDir('Próxima Página >>', base + proxima, 22, artfolder + 'proxpag.jpg')
		except :
				pass
		
def doPlay(url, name, iconimage):
		link = openURL(url)
		
		qlds = ['Qualidade SD', 'Qualidade HD']
		urls = re.compile('ipadUrl: "(.*?)",').findall(link)
		
		if not urls : return
		
		index = 0
		
		if len(urls) > 1 :
				index = xbmcgui.Dialog().select('Selecione a resolução desejada :', qlds)
				
				if index == -1 : return
		
		urlVideo = urls[index]
		
		playlist = xbmc.PlayList(1)
		
		playlist.clear()
		
		listitem = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
		listitem.setInfo("Video", {"Title":name})
		listitem.setProperty('mimetype', 'video/mp4')
		listitem.setProperty('IsPlayable', 'true')

		playlist.add(urlVideo,listitem)
		xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
		xbmcPlayer.play(playlist)

def doPesquisa():
		keyb = xbmc.Keyboard('', 'Pesquisar...')
		keyb.doModal()

		if (keyb.isConfirmed()):
			search = keyb.getText()
			busca = urllib.quote(search)
			url = base + '/busca/?search_query=%s&tipo=desc' % busca
			
			getLancamentos(url)

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

if   mode == None : menuPrincipal()
elif mode == 10   :	getGeneros(url)
elif mode == 11   :	getAnimesGen(url)
elif mode == 20   :	getLancamentos(url)
elif mode == 30   :	getLegendados(url)
elif mode == 31   :	getEpsLegendados(url)
elif mode == 99   : doPesquisa()
elif mode == 100  :	doPlay(url, name, iconimage)

xbmcplugin.setContent(int(sys.argv[1]), 'movies')
xbmcplugin.endOfDirectory(int(sys.argv[1]))
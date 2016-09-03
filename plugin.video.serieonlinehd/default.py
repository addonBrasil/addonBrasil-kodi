#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# By AddonBrasil 26/08/2016
############################################################################################################

import urllib, urllib2, re, xbmcplugin, xbmcgui, xbmc, xbmcaddon, os, datetime
import urlresolver, urlparse

from resources.lib.BeautifulSoup import BeautifulSoup
from resources.lib               import client
from datetime                    import datetime

addon_id    = 'plugin.video.serieonlinehd'
selfAddon   = xbmcaddon.Addon(id=addon_id)
datapath    = xbmc.translatePath(selfAddon.getAddonInfo('profile'))
addonfolder = selfAddon.getAddonInfo('path')
artfolder   = addonfolder + '/resources/img/'
icon        = addonfolder + '/icon.png'
fanart      = addonfolder + '/fanart.jpg'
base        = 'http://www.serieonlinehd.com'

try    : os.mkdir(datapath)
except : pass

try    : getVis  = selfAddon.getSetting('enVis')
except : getVis = 'false'
		
try    : getPlot = selfAddon.getSetting('enableMeta')
except : getPlot = 'true'
		

############################################################################################################

def menuPrincipal():
		addDir('Categorias'        , base                  ,  10, artfolder + 'categorias.png')
		addDir('Séries'            , base + '/serie/'      ,  20, artfolder + 'series.png')
		addDir('Episódios Recentes', base + '/episodio'    ,  30, artfolder + 'new.png')
		addDir('Séries por Ano'    , base                  ,  40, artfolder + 'calend.png')
		addDir('Pesquisa'          , '--'                  , 900, artfolder + 'pesquisa.png')
		addDir('Configurações'     , base                  , 999, artfolder + 'config.png', 1, False)
		
		if getVis == 'true' : setViewMenu()	
		
def getCategorias(url):
		link  = openURL(url)
		soup  = BeautifulSoup(link)
		
		conteudo   = soup("div", {"class": "categorias"})
		categorias = conteudo[0]("li")
		
		totC = len(categorias)
		
		for categoria in categorias:
			titC = categoria.a.text.replace('&amp;','&').encode('utf-8', 'ignore')
			urlC = categoria.a["href"]
			imgC = artfolder + 'categorias.png'
						
			addDir(titC, urlC, 20, imgC)
		
		if getVis == 'true' : setViewMenu()		
		
def getSeries(url):
	link   = openURL(url)
	soup   = BeautifulSoup(link)
	cont   = soup("div", {"class": "item_1 items"})
	series = cont[0]("div", {"class": "item"})
	
	totS = len(series)
	
	for serie in series:
		titS = serie.img["alt"].replace('&#8211;','-').encode('utf-8', 'ignore')
		urlS = serie.a["href"]
		imgS = serie.img["src"]
		
		if getPlot == 'true' :
				plotS = re.findall('<span class="ttx">(.*?)</span>', str(serie), re.MULTILINE|re.DOTALL)[0]
				plotS = plotS.replace('<div class="degradado"></div>','').replace('Sinopse e detalhes '+titS,'').strip()
		else :
				plotS = ''
				
		addDirS(titS, urlS, 21, imgS, True, totS,plotS)
			
	try : 
		proxima = re.findall("<link rel='next' href='(.*?)' />", link)[0]
		addDir('Próxima Página >>', proxima, 20, artfolder + 'proxima.png')
	except : 
		pass
			
	if getVis == 'true' : setViewSeries()
	
def getTemporadas(name,url,iconimage):
	link = openURL(url)

	temps = re.findall('<span class="title">(.*?)</span></div>', link)
	
	totT = len(temps)
	
	for tit in temps:
		titT = tit.encode('utf-8', 'ignore')
		urlT = url
		imgT = iconimage
		
		addDirS(titT, urlT, 22, imgT, True, totT)

	if getVis == 'true' : setViewTemps()
	
def getEpisodios(name,url,iconimage):
	titX = name.split(' - ')[0]
	temp = name[-1:]
	link = openURL(url)
	soup = BeautifulSoup(link)
	cont = soup("div", {"id": "seasons"})
	eps  = cont[0]("li")
	totE = len(eps)
	
	i = 1
	
	for ep in eps:
		epX = re.findall('<div class="numerando">(.*?) x (.*?)</div>', str(ep))[0]

		if str(epX[0]) == str(temp) :
			seaE   = epX[0] 
			epE    =  epX[1] 
			seaepE = seaE + "x" + epE
			titE   = titX + " - " + seaepE + " - " + ep.a.text.encode('utf-8', 'ignore')
			urlE   = ep.a["href"]
			imgE   = iconimage
			
			addDirE(titE, urlE, 100, imgE, False, totE)
			i += 1
			
	if getVis == 'true' : setViewEps()
	
def getRecentes(url):
	link  = openURL(url)
	soup  = BeautifulSoup(link)
	cont  = soup("div", {"id": "episodes"})
	eprec = cont[0]("td", {"class": "bb"})
	
	totEPR = len(eprec)
	
	for ep in eprec:
		if not 'TV Show' in ep :
			rtit = re.findall('<a href=".*?">(.*?)</a>.*?<span>(.*?)</span>', str(ep))[0]
			rtit2 = re.findall('<a href=".*?"><h2>(.*?)</h2></a>', str(ep))[0]
			rimg = re.findall('<div class="imagen"><a href="(.*?)"><img src=" (.*?)" />', str(ep))[0]
		
			titEPR = rtit[0] + ' - ' + rtit[1] + " - " + rtit2
			urlEPR = rimg[0]
			imgEPR = rimg[1]
			
			if getPlot == 'true' :
				rplot = re.findall('<p>(.*?)</p>', str(ep))[0]
				plotEPR = rplot
			else :
				plotEPR = ''
				
			addDirS(titEPR, urlEPR, 100, imgEPR, False, totEPR, plotEPR)
			
	try : 
		proxima = re.findall("<link rel='next' href='(.*?)' />", link)[0]
		addDir('Próxima Página >>', proxima, 30, artfolder + 'proxima.png')
	except : 
		pass

	if getVis == 'true' : setViewEps()
	
def getAnos(url) :
	link = openURL(url)
	soup = BeautifulSoup(link)
	cont = soup("div", {"class": "filtro_y"})
	anos = cont[0]("li")
	
	totA = len(anos)
	
	for ano in anos:
		titA = ano.text.encode('utf-8', 'ignore')
		urlA = ano.a["href"].encode('utf-8', 'ignore')
		imgA = artfolder + 'calend.png'
				
		addDir(titA, urlA, 20, imgA)
			
	if getVis == 'true' : setViewMenu()		

def doPesquisa():
	keyb = xbmc.Keyboard('', 'Pesquisar Filmes')
	keyb.doModal()

	if (keyb.isConfirmed()):
		text = keyb.getText()
		pesq = urllib.quote(text)
		url  = base + '/?s=%s' % str(pesq)
		getResults(url)
		
def getResults(url)	:
	link    = openURL(url)
	results = re.findall('<a href="(.*?)"><img src="(.*?)" alt="(.*?)" /></a>', link)
	plots   = re.findall('<div class="contenido"><p>(.*?)</p><div class="degradado">', link, re.MULTILINE|re.DOTALL)
	
	totR = len(results)
	
	i = 0
	
	for urlR, imgR, titR in results:
		titR  = titR.replace('&#8211;','-')
		plotR = plots[i].strip()
		addDirS(titR, urlR, 21, imgR, True, totR, plotR)
		i = i + 1
			
	if getVis == 'true' : setViewSeries()
				
def player(name,url,iconimage):
	mensagemprogresso = xbmcgui.DialogProgress()
	
	mensagemprogresso.create('SÉRIE ONLINE HD', 'Obtendo fonte para ' + name, 'Por favor aguarde...')
	mensagemprogresso.update(0)
	
	link = openURL(url)
	vmID  = re.findall('".*?hashkey=(.*?)"', link)[0]
	urlVM = 'http://videomega.tv/cdn.php?ref=%s' % vmID
	
	mensagemprogresso.update(25,'Resolvendo fonte para ' + name, 'Por favor aguarde...')

	urlVideo = urlresolver.resolve(urlVM)
	
	mensagemprogresso.update(50,'Obtendo legendas para ' + name, 'Por favor aguarde...')
	
	legendas = getLegenda(urlVM+'&val=1')
	
	mensagemprogresso.update(75,'Abrindo sinal para ' + name, 'Por favor aguarde...')
	
	playlist = xbmc.PlayList(1)
	playlist.clear()
	
	listitem = xbmcgui.ListItem(name,thumbnailImage=iconimage)
	
	listitem.setPath(urlVideo)
	listitem.setProperty('mimetype','video/mp4')
	listitem.setProperty('IsPlayable', 'true')
	
	playlist.add(urlVideo,listitem)
	
	xbmcPlayer = xbmc.Player()
	xbmcPlayer.play(playlist)

	mensagemprogresso.update(100)
	mensagemprogresso.close()
	
	if legendas != '-' : xbmcPlayer.setSubtitles(legendas)
		
def getLegenda(url):
	try:
		url = urlparse.urlparse(url).query
		url = urlparse.parse_qsl(url)[0][1]
		url = 'http://videomega.tv/cdn.php?ref=%s' % url

		result = client.request(url, mobile=True)
		
		sub = client.parseDOM(result, 'track' , ret='src')[0]
		
		return sub 
	except:
		return '-'

############################################################################################################

def openConfig():
	selfAddon.openSettings()
	xbmc.executebuiltin("Container.Refresh()")

def openURL(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	
	return link

def addDir(name, url, mode, iconimage, total=1, pasta=True):
	u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
	
	ok = True
	
	liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
	
	liz.setProperty('fanart_image', fanart)
	liz.setInfo(type = "Video", infoLabels = {"title": name})
	
	ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=pasta, totalItems=total)

	return ok
		
def addDirS(name,url,mode,iconimage,pasta=True,total=1, plot='') :
	u  = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
	ok = True
	
	liz = xbmcgui.ListItem(name, iconImage="iconimage", thumbnailImage=iconimage)
	
	liz.setProperty('fanart_image', iconimage)
	liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": plot})
	
	ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)

	return ok	

def addDirE(name,url,mode,iconimage,pasta=True,total=1) :
	u   = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
	ok  = True
	liz = xbmcgui.ListItem(name, iconImage="iconimage", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', iconimage)
	liz.setInfo(type="Video", infoLabels={"Title": name})
	ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
	
	return ok	
		
def setViewMenu() :
	skin = xbmc.getSkinDir()
	
	try    : opcao = selfAddon.getSetting('menuVisu')
	except : opcao == 'Icons'
		
	if 'skin.confluence' in skin :
		if   opcao == 'Icons'    : VM = 500
		elif opcao == 'List'     : VM = 50
		elif opcao == 'Low List' : VM = 503
		
	elif 'skin.aeon.nox' in skin:
		if   opcao == 'Icons'    : VM = 500
		elif opcao == 'List'     : VM = 50
		elif opcao == 'Low List' : VM = 504
		
	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	xbmc.executebuiltin('Container.SetViewMode(%d)' % VM)

def setViewSeries() :
	skin  = xbmc.getSkinDir()
	
	try    : opcao = selfAddon.getSetting('seriesVisu')
	except : opcao == 'Icons'
	
	if 'skin.confluence' in skin :
		if   opcao == 'Icons'       : VM = 500
		elif opcao == 'Info'        : VM = 515
		elif opcao == 'Fanart'      : VM = 508
		elif opcao == 'List'        : VM = 50
		elif opcao == 'Poster Wrap' : VM = 501
		
	elif 'skin.aeon.nox' in skin:
		if   opcao == 'Icons'       : VM = 500
		elif opcao == 'Info'        : VM = 55
		elif opcao == 'Fanart'      : VM = 602
		elif opcao == 'List'        : VM = 50
		elif opcao == 'Poster Wrap' : VM = 56

	xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
	xbmc.executebuiltin('Container.SetViewMode(%d)' % VM)
		
def setViewTemps() :
	skin  = xbmc.getSkinDir()
	
	try    : opcao = selfAddon.getSetting('tempsVisu')
	except : opcao == 'Icons'

	if 'skin.confluence' in skin :
		if   opcao == 'Icons'      : VM = 500
		elif opcao == 'List'       : VM = 50
		
	elif 'skin.aeon.nox' in skin:
		if   opcao == 'Icons'      : VM = 500
		elif opcao == 'List'       : VM = 50

	xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
	xbmc.executebuiltin('Container.SetViewMode(%d)' % VM)
	
def setViewEps() :
	skin  = xbmc.getSkinDir()
	
	try    : opcao = selfAddon.getSetting('epsVisu')
	except : opcao == 'Icons'
	
	if 'skin.confluence' in skin :
		if   opcao == 'Icons'      : VM = 500
		elif opcao == 'Info'       : VM = 515
		elif opcao == 'List'       : VM = 50
		elif opcao == 'Low List'   : VM = 503
		elif opcao == 'Big List'   : VM = 51
		
	elif 'skin.aeon.nox' in skin:
		if   opcao == 'Icons'      : VM = 500
		elif opcao == 'Info'       : VM = 55
		elif opcao == 'List'       : VM = 50
		elif opcao == 'Low List'   : VM = 501
		elif opcao == 'Big List'   : VM = 510

	xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
	xbmc.executebuiltin('Container.SetViewMode(%d)' % VM)

############################################################################################################
              
def get_params():
		param=[]
		paramstring=sys.argv[2]
		
		if len(paramstring)>=2:
				params=sys.argv[2]
				cleanedparams=params.replace('?','')
				
				if (params[len(params)-1]=='/') : params=params[0:len(params)-2]
				
				pairsofparams=cleanedparams.split('&')
				param={}
				
				for i in range(len(pairsofparams)):
						splitparams={}
						splitparams=pairsofparams[i].split('=')
						
						if (len(splitparams))==2 : param[splitparams[0]]=splitparams[1]
														
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

try    : mode=int(params["mode"])
except : pass

try    : iconimage=urllib.unquote_plus(params["iconimage"])
except : pass

###############################################################################################################
#                                                   MODOS                                                     #
###############################################################################################################

if   mode == None : menuPrincipal()
elif mode == 10   : getCategorias(url)
elif mode == 20   : getSeries(url)
elif mode == 30   : getRecentes(url)
elif mode == 21   : getTemporadas(name,url,iconimage)
elif mode == 22   : getEpisodios(name,url,iconimage)
elif mode == 40   : getAnos(url)
elif mode == 100  : player(name,url,iconimage)
elif mode == 900  : doPesquisa()
elif mode == 999  : openConfig()

xbmcplugin.endOfDirectory(int(sys.argv[1]))	



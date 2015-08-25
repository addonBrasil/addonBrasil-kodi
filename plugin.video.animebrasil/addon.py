#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# By AddonBrasil - 24/08/15

#########################################################################

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,HTMLParser,sys
from xbmcgui import ListItem
from BeautifulSoup import BeautifulSoup

versao      = '1.0.0'
addon_id    = 'plugin.video.animebrasil'
selfAddon   = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder   = addonfolder + '/resources/img/'
fanart      = addonfolder + '/fanart.jpg'
base        = 'http://anitubebr.xpg.uol.com.br/'

def menuPrincipal():
	addDir2('Categorias'    , base + 'categories'     , 10, artfolder + 'categorias.jpg')
	addDir2('+ Recentes'    , base + 'videos/basic/mr', 20, artfolder + 'recentes.jpg')
	addDir2('+ Visualizados', base + 'videos/basic/mv', 20, artfolder + 'visualizados.jpg')
	addDir2('+ Comentados'  , base + 'videos/basic/md', 20, artfolder + 'comentados.jpg')
	addDir2('+ Populares'   , base + 'videos/basic/tr', 20, artfolder + 'populares.jpg')
	addDir2('Top Favoritos' , base + 'videos/basic/tf', 20, artfolder + 'favoritos.jpg')
	addDir2('Em Destaque'   , base + 'videos/basic/rf', 20, artfolder + 'destaque.jpg')
	addDir2('Pesquisa'      , base                    , 30, artfolder + 'pesquisa.jpg')
	
	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	xbmc.executebuiltin('Container.SetViewMode(50)')

def getCategorias(url):
		link = openURL(url)
		link = unicode(link, 'utf-8', errors='ignore')
		
		soup = BeautifulSoup(link)
		categorias = soup.findAll("li", { "class" : "mainList" })

		a = []
		
		for categoria in categorias:
				urlTemp  = categoria.a["href"]
				titTemp  = categoria.a.img["alt"].encode('ascii', 'ignore')
				imgTemp  = categoria.a.img["src"]
				plotTemp = categoria.a["title"].replace('Sinopse:', '').replace('Sinopse; ', '')
				temp = [urlTemp, titTemp,imgTemp,plotTemp] 
				a.append(temp)
				
		total = len(a)

		for url2, titulo, img, plot in a:
				titulo = cleanHtml(titulo).replace(' category','')
				addDir(titulo,url2,20,img,True,total,plot)
			
		pages = soup.find('ul',{ "id" : "pagination-flickr" }).findAll('a')
		
		for prox_pagina in pages:
				if prox_pagina.text == 'Next':
						addDir('Próxima Página >>',prox_pagina['href'],10,artfolder + 'proxpag.jpg')
				
		xbmcplugin.setContent(int(sys.argv[1]), 'movies')
		xbmc.executebuiltin('Container.SetViewMode(515)')

def getEpisodios(url):
		link = openURL(url)
		link = unicode(link, 'ascii', errors='ignore')
		
		soup = BeautifulSoup(link)
		episodios = soup.findAll("li", { "class" : "mainList" })

		e = []
		
		for episodio in episodios:
				try:
						titTemp = episodio.a.img["alt"].encode('ascii', 'ignore')
						urlTemp = episodio.a["href"]
						imgTemp = episodio.a.img['src']
						temp = [titTemp, urlTemp ,imgTemp, ''] 
						e.append(temp)
				except:
						pass
				
		print "NÃO SORT " + str(e)
		e.sort()
		print "SORT " + str(e)
		
		total = len(e)

		for titulo, url2, img, plot in e:
				titulo = cleanHtml(titulo)
				addDir(titulo, url2, 100, img, False, total, plot)
				
		try:
				pages = soup.find('ul',{ "id" : "pagination-flickr" }).findAll('a')
				
				for prox_pagina in pages:
						if prox_pagina.text == 'Next':
								addDir('Próxima Página >>',prox_pagina['href'],20,artfolder + 'proxpag.jpg')
		except:
				pass
				
		xbmcplugin.setContent(int(sys.argv[1]), 'movies')
		xbmc.executebuiltin('Container.SetViewMode(500)')

def doPlay(url, name, iconimage):
		link = openURL(url)
		jwpURL = re.findall(r'<script type="text/javascript" src="http://anitubebr.xpg.uol.com.br/player/config.php\?key=(.*?)"></script>',link)[0]
		jwpURL = 'http://anitubebr.xpg.uol.com.br/player/config.php?key=' + jwpURL
		
		jwp = openURL(jwpURL)
		
		urlx = re.compile('file: "(.*?).mp4"').findall(jwp)
		qldx = re.compile('label: "(.*?)"').findall(jwp)
			
		print "URLX = " + str(urlx)
		print "QLDX = " + str(qldx)
		
		urls = []
		qlds = []
		
		toturls = len(urlx)
		
		i = 0
		
		for i in range(toturls) :
				if urlx[i] == '' :
					i += 1	
				else :
						urls.append(urlx[i])
						qlds.append(qldx[i])
						i += 1
		
		if not urls : return
		
		index = xbmcgui.Dialog().select('Selecione a resolução desejada :', qlds)

		if index == -1 : return

		urlTemp = urls[index]
		
		urlVideo = urlTemp.replace('//vid','//iad').replace('cdn','vid') + '.mp4'
		
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
			url = 'http://anitube.xpg.uol.com.br/search/?search_id=' + str(busca)
			getEpisodios(url)

###################################################################################

def addLink(name,url,iconimage):
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', fanart)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok

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

def cleanHtml(dirty):
    clean = re.sub('&quot;', '\"', dirty)
    clean = re.sub('&#039;', '\'', clean)
    clean = re.sub('&#215;', 'x', clean)
    clean = re.sub('&#038;', '&', clean)
    clean = re.sub('&#8216;', '\'', clean)
    clean = re.sub('&#8217;', '\'', clean)
    clean = re.sub('&#8211;', '-', clean)
    clean = re.sub('&#8220;', '\"', clean)
    clean = re.sub('&#8221;', '\"', clean)
    clean = re.sub('&#8212;', '-', clean)
    clean = re.sub('&amp;', '&', clean)
    clean = re.sub("`", '', clean)
    clean = re.sub('<em>', '[I]', clean)
    clean = re.sub('</em>', '[/I]', clean)
    return clean	

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

print "Mode     : " + str(mode)
print "URL      : " + str(url)
print "Name     : " + str(name)
print "Iconimage: " + str(iconimage)

if   mode == None : menuPrincipal()
elif mode == 10   :	getCategorias(url)
elif mode == 20   :	getEpisodios(url)
elif mode == 30   : doPesquisa()
elif mode == 100  :	doPlay(url, name, iconimage)
	
xbmcplugin.endOfDirectory(int(sys.argv[1]))
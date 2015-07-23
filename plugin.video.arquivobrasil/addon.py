# -*- coding: utf-8 -*-
# Copyright 2015 AddonBrasil
#
#####################################################################

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,HTMLParser
import httplib, mechanize, base64

from urlparse      import urlparse
from BeautifulSoup import BeautifulSoup
#from BeautifulSoup import BeautifulStoneSoup, BeautifulSoup, BeautifulSOAP

h = HTMLParser.HTMLParser()

versao      = '1.0.1'
addon_id    = 'plugin.video.arquivobrasil'
selfAddon   = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')

icon      = addonfolder + '/icon.png'
fanart    = addonfolder + '/fanart.jpg'
artfolder = addonfolder + '/resources/art/'

base = 'https://www.assistirnovelas.tv'

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
		
		conteudo = soup("div", {"class": "Box"})
		
		if name   == 'Novelas'    : temp = conteudo[0]
		elif name == 'Séries'     : temp = conteudo[1]
		elif name == 'Jornalismo' : temp = conteudo[2]
		elif name == 'Variedades' : temp = conteudo[3]
		elif name == 'Esportes'   : temp = conteudo[4]
		
		listaCateg = temp("li")
		
		totLista = len(listaCateg)
		
		for categoria in listaCateg:
				titcat = categoria.img["alt"].replace('Assistir ', '').encode('utf-8')
				urlcat = categoria.a["href"]
				imgcat = categoria.img["src"]
				addDir(titcat, urlcat, 20, imgcat, totLista, True)				

		xbmc.executebuiltin('Container.SetViewMode(500)')
		
def getVideosCat(url, name, iconimage):
		link   = openURL(url)
		soup   = BeautifulSoup(link)
		videos = soup("div", {"class": "Imagem"})

		totVideos = len(videos)

		for video in videos:
				url = video.a["href"]
				tit = video.img["alt"].replace('Assistir ', '').encode('utf-8', 'ignore')
				img = video.img["src"] 
				addDir(tit, url, 100, img, False, totVideos)

		try:
				pagina = BeautifulSoup(soup.find('div', { "class" : "Paginacao" }).prettify())("a", { "class" : "right" })[0]["href"]
				addDir("Proxima Pagina >>", pagina, 20, artfolder + "proxima.jpg", totVideos + 1)
		except:
				pass				
				
		xbmc.executebuiltin('Container.SetViewMode(50)')

def doPlay(url, name):
		pg = 0
		msgDialog = xbmcgui.DialogProgress()

		msgDialog.create('ARQUIVO BRASIL', 'Criando Playlist',name,'Por favor aguarde...')
		pg += 10
		msgDialog.update(pg)
		
		link = openURL(url)
		soup = BeautifulSoup(link)
		
		playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
		playlist.clear()

		pg += 20
		msgDialog.update(pg)

		browser = mechanize.Browser()
		
		browser.set_handle_equiv(True)
		browser.set_handle_redirect(True)
		browser.set_handle_referer(True)
		browser.set_handle_robots(False)
		browser.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
		
		browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
		browser.addheaders = [('Referer', url)]
		
		pg += 20
		msgDialog.update(pg)
		
		browser.open(base)
		form = base64.b64decode('PGZvcm0gYWN0aW9uPSJodHRwczovL2Fzc2lzdGlybm92ZWxhcy50di9Mb2dpblVzdWFyaW8ucGhwIiBpZD0iZm9ybTEiIG1ldGhvZD0icG9zdCI+DQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxsaT5FLW1haWw8L2xpPg0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8bGk+PGlucHV0IHR5cGU9InRleHQiIHZhbHVlPSIiIG5hbWU9ImVtYWlsIiBjbGFzcz0iQ2FtcG9Mb2dpbiIgcGxhY2Vob2xkZXI9IlNldSBlLW1haWwiPjwvbGk+DQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxsaT5TZW5oYTwvbGk+DQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxsaT48aW5wdXQgdmFsdWU9IiIgbmFtZT0ic2VuaGEiIGNsYXNzPSJDYW1wb0xvZ2luIiBwbGFjZWhvbGRlcj0iU3VhIHNlbmhhIiB0eXBlPSJwYXNzd29yZCI+PC9saT4NCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPGxpPjxpbnB1dCB0eXBlPSJzdWJtaXQiIGNsYXNzPSJMb2dpbkluaWNpbyIgdmFsdWU9IkVudHJhciI+PC9saT4NCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPGxpPjxhIGhyZWY9Imh0dHBzOi8vYXNzaXN0aXJub3ZlbGFzLnR2L2NhZGFzdHJvLnBocCI+UmVnaXN0cmFyPC9hPjwvbGk+DQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxsaT48YSBocmVmPSJodHRwczovL2Fzc2lzdGlybm92ZWxhcy50di9sZW1icmFyX3NlbmhhLnBocCI+TGVtYnJhciBzZW5oYTwvYT48L2xpPg0KICAgICAgICAgICAgICAgICAgPC9mb3JtPg==')
		res  = mechanize._form.ParseString(form, base)
		
		browser.form = res[1]
		
		browser.form['senha'] = base64.b64decode('YXJhbW9zIUAj')
		browser.form['email'] = base64.b64decode('YWRtaW5AYWRkb25icmFzaWwudGs=')
		browser.submit()

		pg += 20
		msgDialog.update(pg)

		pgbrowser = browser.open(url).read()
		iframe    = re.findall("var url = '(.*?)'", pgbrowser)[0]+"html5iframe/"
		
		pglinks = browser.open(iframe).read()
		
		vars = re.findall("var (.*?) \= \[(.*?)\]", pglinks)
		
		decvars = []
		
		x = 0
		
		for x in range(len(vars)) :
				id = str(vars[x][0])
				aut = str(vars[x][1])
				aut = aut.replace('\"','').replace(',','')
				decvars.append([id,aut])
				x += 1
		
		links = re.findall('return\(\[(.*?)\]\.join\(\"\"\) \+ (.*?)\.join\(\"\"\)', pglinks)
                          
		pg += 10
		msgDialog.update(pg)
		
		if links:
				for link in links:
						link2play = link[0].replace('\"','').replace(',','').replace('\\','')
						x = 0
						for x in range(len(decvars)) :
								if link[1] == decvars[x][0]:
										break
								else :
									x += 1
									
						link2play = link2play + decvars[x][1]
						liz = xbmcgui.ListItem(name, thumbnailImage=iconimage)
						liz.setInfo('video', {'Title': name})
						playlist.add(url=link2play, listitem=liz, index=7)
						
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
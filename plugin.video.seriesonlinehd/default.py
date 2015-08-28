#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# By AddonBrasil - 26/08/15
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
				proxpag = BeautifulSoup(soup.find('div', { "class" : "wp-pagenavi" }).prettify())("a", { "class" : "previouspostslink" })[0]["href"]
				if 'miss' in proxpag :
						print "sim tem"
						temp = proxpag.partition('?')
						print temp
						proxpag = temp[0]
				print proxpag
				addDir2("Próxima Página >>", proxpag, 10, artfolder + "proxima.jpg",fanart)
		except:
				pass
				
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

		xbmc.executebuiltin('Container.SetViewMode(50)')

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
						
						if 'Episódio' in epsE :
								titEpisodioT =  seaE + ' - ' + epsE 
						else : 
								titEpisodioT =  seaE + ' - Episódio ' + epsE 
						
						if dubE != '' : 
								titEpisodio = titEpisodioT + ' - Dublado' #+ ' - ' + resE
								addDir2(titEpisodio, dubE, 100, iconimage, fanart, False)
						if legE != '' : 
								titEpisodio = titEpisodioT + ' - Legendado' #+ ' - ' + resE
								addDir2(titEpisodio, legE, 100, iconimage, fanart,False)
						
				e += 1
				
		xbmc.executebuiltin('Container.SetViewMode(500)')
				
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
		cloudzilla = r'href=".*?cz.php\?cz=(.*?)"'
		#dropvideo  = r'href=".*?dv.php\?dv=(.*?)-800x400.html"'
		#dropvidhd  = r'href=".*?dvhd.php\?dvhd=(.*?)-800x400.html"'
		ok         = r'href="(.*?ok2.php\?key=.*?)"'
		videopw    = r'href=".*?vpw.php\?vpw=(.*?)"'
		vidtome    = r'href=".*?vt.php\?vt=(.*?)-800x400.html"'
		
		mensagemprogresso = xbmcgui.DialogProgress()
		mensagemprogresso.create('Séries Online HD', 'Resolvendo Link','Por favor aguarde...')
		mensagemprogresso.update(33)

		links = []
		hosts = []
		matriz = []

		link = openURL(url)
		
		try:
				links.append('http://www.cloudzilla.to/embed/'+re.findall(cloudzilla, link)[0])
				hosts.append('CLOUDZILLA')
		except:
				pass

		try:
				links.append(re.findall(ok, link)[0])
				hosts.append('OK')
		except:
				pass
				
		try:
				links.append('http://videopw.com/e/'+re.findall(videopw, link)[0])
				hosts.append('VIDEOPW')
		except:
				pass

		try:
				links.append('http://www.vidto.me/'+re.findall(vidtome, link)[0])
				hosts.append('VIDTO.ME')
		except:
				pass

		if not hosts :	return

		index = xbmcgui.Dialog().select('Selecione um dos hosts suportados :', hosts)

		if index == -1 : return

		url_video = links[index]
		mensagemprogresso.update(66)

		print 'Player url: %s' % url_video

		if   'cloudzilla' in url_video : matriz = getVideoURL(url_video)	
		elif 'ok'         in url_video : matriz = getOK(url_video)   
		elif 'videopw'    in url_video : matriz = getVideoPW(url_video)   
		elif 'vidto'      in url_video : matriz = getVideoURL(url_video)   
		else                           : print "Falha: " + str(url_video)
			
		url = matriz[0]

		if url=='-': return

		legendas = matriz[1]

		print "Url do gdrive: " + str(url_video)
		print "Legendas: " + str(legendas)

		mensagemprogresso.update(100)
		mensagemprogresso.close()

		playlist = xbmc.PlayList(1)
		playlist.clear()
		listitem = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
		listitem.setInfo("Video", {"Title":name})
		listitem.setProperty('mimetype', 'video/x-msvideo')
		playlist.add(url,listitem)
		xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
		xbmcPlayer.play(playlist)

		if legendas != '-':
				if 'timedtext' in legendas:
						import os.path
						sfile = os.path.join(xbmc.translatePath("special://temp"),'sub.srt')
						sfile_xml = os.path.join(xbmc.translatePath("special://temp"),'sub.xml')#timedtext
						sub_file_xml = open(sfile_xml,'w')
						sub_file_xml.write(urllib2.urlopen(legendas).read())
						sub_file_xml.close()
						print "Sfile.srt : " + sfile_xml
						xmltosrt.main(sfile_xml)
						xbmcPlayer.setSubtitles(sfile)
				else:
						xbmcPlayer.setSubtitles(legendas)
						
#############################################################################################

def getVideoURL(vURL) :
		urlVideo = urlresolver.HostedMediaFile(url=vURL).resolve()
		
		if urlVideo : return [urlVideo, '-']
		else        : return ['-', '-']
		
def getDropVideo(url):
		link = openURL(url)
		
		try:
				soup  = BeautifulSoup(link)
				lista = soup.findAll('script')
				js    = str(lista[9]).replace('<script>',"").replace('</script>',"")
				
				sUnpacked = jsunpack.unpack(js)
				url_video = re.findall(r'var vurl2="(.*?)";', sUnpacked)
				url_video = str(url_video).replace("['","").replace("']","")
				return [url_video,"-"]
		except:
				pass	
				
def getOK(url) :
		legVideo = '-'
		urlVideo = '-'
		
		link = openURL(url)

		urlx = re.compile("'file': '(.*?)'").findall(link)
		qldx = re.compile("'label': '(.*?)'").findall(link)
		
		try :
				legx = re.findall(r'file: "(/legendas/.*?)"', link)[0]
				
				if legx <> '' : legVideo = base + str(legx)
				else          : legVideo = '-'
		except :
				pass
				
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
		
		if not urls : return [urlVideo, legVideo]
		
		index = xbmcgui.Dialog().select('Selecione a resolução desejada :', qlds)

		if index == -1 : return [urlVideo, legVideo]

		urlVideo = urls[index]
		
		return [urlVideo, legVideo]
		
def getVideoPW(url) :
		link = openURL(url)

		try:
			urlVideoPW = re.findall(r'vurl2 = "(.+?)";',link)[0]
			urlLegVPW  = re.findall(r'vsubtitle = "(.+?)";',link)[0]
			urlVideo    = urlVideoPW
			urlLegendas = urlLegVPW
		except:
			urlVideo    = '-'
			urlLegendas = '-'
			
		return [urlVideo, urlLegendas]			
		
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


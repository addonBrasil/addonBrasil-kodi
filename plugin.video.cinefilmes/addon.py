# -*- coding: UTF-8 -*-
#
# By AddonBrasil 08/12/2015
# Atualização 1.0.3: 29/12/2015
############################################################################################################

import urllib, urllib2, urlparse, re, xbmcplugin, xbmcgui, xbmc, xbmcaddon, os, time
import urlresolver, json

from resources.lib.BeautifulSoup import BeautifulSoup
from resources.lib               import client
from resources.lib               import jsunpack
from resources.lib               import control

addon_id    = 'plugin.video.cinefilmes'
selfAddon   = xbmcaddon.Addon(id=addon_id)
datapath    = xbmc.translatePath(selfAddon.getAddonInfo('profile'))
addonfolder = selfAddon.getAddonInfo('path')
artfolder   = addonfolder + '/resources/img/'
icon        = addonfolder + '/icon.png'
fanart      = addonfolder + '/fanart.jpg'

base = 'http://www.cinefilmeshd.com'

############################################################################################################

def menuPrincipal():
		addDir('Categorias'        , base                ,  10, artfolder + 'categorias.png')
		addDir('Lançamentos'       , base + '/lancamento',  20, artfolder + 'new.png')
		addDir('Filmes 1080p'      , base + '/1080p'     ,  20, artfolder + 'filmes.png')
		addDir('Filmes Bluray'     , base + '/bluray'    ,  20, artfolder + 'filmes.png')
		addDir('Filmes Legendados' , base + '/legendados',  20, artfolder + 'filmes.png')
		addDir('Séries'            , base                ,  30, artfolder + 'series.png')
		addDir('Pesquisa de Filmes', '--'                ,  40, artfolder + 'pesquisa.png')
		addDir('Configurações'     , base                , 999, artfolder + 'config.png', 1, False)
			
		setViewMenu()	
		
def getCategorias(url):
		link  = openURL(url)
		soup  = BeautifulSoup(link)
		
		conteudo   = soup("div", {"class": "row aling"})
		categorias = conteudo[0]("a")
		
		totC = len(categorias)
		
		for categoria in categorias:
				titC = categoria.img['title']
				titC = titC.replace('Filmes na categoria: ','').replace('Categoria: ','').replace('categoria: ','').encode('utf-8', 'ignore')
				
				if not ("Todas" in titC or "Filmes" in titC or "Seriados" in titC or "Em Breve" in titC or "Lançamentos" in titC or "Novos" in titC) :
						urlC = categoria['href']
						imgC = categoria.img['src']
						
						addDir(titC, urlC, 20, imgC)
				
		setViewMenu()		
		
def getFilmes(url):
		link  = openURL(url)
		link = unicode(link, 'utf-8', 'ignore')		

		soup  = BeautifulSoup(link)
		
		conteudo = soup("div", {"class": "rel-single"})
		filmes   = conteudo[0]("li")
		
		totF = len(filmes)
		
		for filme in filmes:
				try    : titF = filme.img["title"].encode('latin1').encode('utf-8','ignore')
				except : titF = filme.img["title"].encode('utf-8','ignore')
					
				titF = titF.replace('Dublado - 1080p','').replace('Dublado - 720p','').replace('Legendado - 1080p','').replace('Legendado - 720p','')
				urlF = filme.a["href"]
				imgF = filme.img["src"]. replace(base + "/wp-content/themes/CineFilmes3/timthumb.php?src=","")
				pltF = re.findall('<div class="sinopse-box">(.*?)</div>', str(filme))[0]
				
				try    :	pltF = pltF.split('&#8211;')[1]
				except :	pass
						
				try    : pltF = pltF.encode('latin1').decode('utf-8')
				except : pltF = pltF.decode('utf8')
					
				addDirF(titF, urlF, 100, imgF, False, totF, pltF)
				
		try : 
				proxima = re.findall('<a class="next page-numbers" href="(.*?)">', link)[0]
				addDir('Próxima Página >>', proxima, 20, artfolder + 'proxima.png')
		except : 
				pass
				
		setViewFilmes()
		
def getAnos(url) :
		link = openURL(url)
		soup = BeautifulSoup(link)
		
		conteudo = soup("div", {"class": "box-seletor"})
		anos     = conteudo[1]("option")
		
		totA = len(anos)
		
		for ano in anos:
				titA = ano.text.encode('utf-8', 'ignore')
				
				if not "Ano" in titA :
						urlA = base + '/?cat=' + ano["value"]
						imgA = artfolder + 'categorias.png'
						
						addDir(titA, urlA, 20, imgA)
				
		setViewMenu()		

def doPesquisa():
		keyb = xbmc.Keyboard('', 'Pesquisar Filmes')
		keyb.doModal()

		if (keyb.isConfirmed()):
				texto    = keyb.getText()
				pesquisa = urllib.quote(texto)
				url      = base + '?s=%s' % str(pesquisa)
				
				getFilmes(url)
				
def player(name,url,iconimage):
		OK = False
		
		nome = name
		msgDP= xbmcgui.DialogProgress()
		
		msgDP.create('CINEFILMES HD', 'Obtendo Fontes Para ' + name, 'Por favor aguarde...')
		msgDP.update(25)
		
		nServers = []
		uServers = []
		matriz = []
		
		link = openURL(url)
		
		iFrame = re.findall('<li class="video1-box" id="video"><iframe src="(.*?)" frameborder="0" scrolling="no" width="100%" height="430" allowfullscreen></iframe>', link)[0]
		
		link = openURL(iFrame)
		
		servers = re.findall("addiframe\('(.*?)'\);", link)
		
		for server in servers :
				if not 'goo' in server :
						if not 'hqq' in server :
								if not 'flashx' in server :
										if not 'thevid' in server :
												if not 'videowood' in server :
															ns = getRegex(server, '//', '/')
															
															if len(ns) > 1 :
																	nServers.append(ns.upper())
																	uServers.append(server)
		
		if not nServers : return
		
		index = xbmcgui.Dialog().select('Selecione uma das fontes suportadas :', nServers)
		
		if index == -1 : return
		
		msgDP.update(50, 'Resolvendo fonte Para ' + name, 'Por favor aguarde...')
		
		url2Resolve = uServers[index]
		
		legendas = '-'
		
		if 'closedload.tk' in url2Resolve :
				link = openURL(url2Resolve)
				urls = re.findall('file: "(.*?)",', link)
				url2Play = urls[0]
				
				legendas = url2Resolve.split('?')[0]
				legendas += urls[1]
				
				OK = True

		elif 'haaze.com.br' in url2Resolve :
				link = openURL(url2Resolve)
				urls = re.findall("<source src='(.*?)' type='video/mp4' /><track kind='subtitles' src='(.*?)' srclang='.*?' label='.*?' default>", link)[0]
				
				url2Play = urls[0]
				
				legendas = url2Resolve.split('watch')[0]
				legendas += urls[1].replace('../','')
				
				OK = True

		elif 'pcloud.com' in url2Resolve :
				link = openURL(url2Resolve)
				
				url2Play = re.findall('"downloadlink": "(.*?)",', link)[0]
				url2Play = url2Play.replace('\/','/')
				
				OK = True
				
		if 'cloudzilla' in url2Resolve :
				if 'www' in url2Resolve : url2Resolve = url2Resolve.replace('www.cloudzilla.to','neodrive.co')
				else                    : url2Resolve = url2Resolve.replace('cloudzilla.to','neodrive.co')
						
		elif 'video.tt' in url2Resolve :
				try    : vttID = url2Resolve.split('embed/')[1]
				except : vttID = url2Resolve.split('e/')[1]
				
				url2Resolve = 'http://www.video.tt/watch_video.php?v=%s' % vttID
				
				OK = True
				
		elif 'videoteca' in url2Resolve :
			link   = openURL(url2Resolve)
			urlV   = re.findall('<iframe src="(.*?)" width=".*?"', link)[0]
			linkVT = openURL(url2Resolve)
			
			url2Resolve = re.findall("'file': '(.*?).mp4',", linkVT)[0]
			url2Play    = url2Resolve + '.mp4'

			OK = True
			
		if not OK : url2Play = urlresolver.HostedMediaFile(url2Resolve).resolve()				

		msgDP.update(75,'Abrindo Sinal Para ' + nome, 'Por favor aguarde...')
		
		playlist = xbmc.PlayList(1)
		playlist.clear()
		
		listitem = xbmcgui.ListItem(name,thumbnailImage=iconimage)
		
		listitem.setPath(url2Play)
		listitem.setProperty('mimetype','video/mp4')
		listitem.setProperty('IsPlayable', 'true')
		
		playlist.add(url2Play,listitem)
		
		xbmcPlayer = xbmc.Player()
		xbmcPlayer.play(playlist)

		msgDP.update(100)
		msgDP.close()
		
		if legendas != '-' : xbmcPlayer.setSubtitles(legendas)
		
def getInfo(url) :
		link  = openURL(url)
		nomeF = re.findall('<li>Titulo Original: <span>(.*?)</span></li>', link)[0]
		xbmc.executebuiltin('XBMC.RunScript(script.extendedinfo,info=extendedinfo,name=%s)' % nomeF)
		
def playTrailer(url):
		link = openURL(url)
		ytID = re.findall('src="http://www.youtube.com/embed/(.*?)"', link)[0]
		xbmc.executebuiltin('XBMC.RunPlugin("plugin://script.extendedinfo/?info=youtubevideo&&id=%s")' % ytID)
	
############################################################################################################

def openConfig():
		selfAddon.openSettings()
		setViewMenu()
		xbmcplugin.endOfDirectory(int(sys.argv[1]))

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
		
def addDirF(name,url,mode,iconimage,pasta=True,total=1,plot='') :
		u  = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
		ok = True
		
		liz = xbmcgui.ListItem(name, iconImage="iconimage", thumbnailImage=iconimage)
		
		liz.setProperty('fanart_image', iconimage)
		liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": plot})
		
		cmItems = []
		
		cmItems.append(('[COLOR lime]Assistir Trailer[/COLOR]', 'XBMC.RunPlugin(%s?url=%s&mode=99)'%(sys.argv[0], urllib.quote_plus(url))))
		
		liz.addContextMenuItems(cmItems, replaceItems=False)
				
		ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
		
		return ok	
		
def setViewMenu() :
		xbmcplugin.setContent(int(sys.argv[1]), 'movies')
		
		opcao = selfAddon.getSetting('menuVisu')
		
		if   opcao == '0': xbmc.executebuiltin("Container.SetViewMode(50)")
		elif opcao == '1': xbmc.executebuiltin("Container.SetViewMode(51)")
		elif opcao == '2': xbmc.executebuiltin("Container.SetViewMode(500)")
		
def setViewFilmes() :
		xbmcplugin.setContent(int(sys.argv[1]), 'movies')

		opcao = selfAddon.getSetting('filmesVisu')

		if   opcao == '0': xbmc.executebuiltin("Container.SetViewMode(50)")
		elif opcao == '1': xbmc.executebuiltin("Container.SetViewMode(51)")
		elif opcao == '2': xbmc.executebuiltin("Container.SetViewMode(500)")
		elif opcao == '3': xbmc.executebuiltin("Container.SetViewMode(501)")
		elif opcao == '4': xbmc.executebuiltin("Container.SetViewMode(508)")
		elif opcao == '5': xbmc.executebuiltin("Container.SetViewMode(504)")
		elif opcao == '6': xbmc.executebuiltin("Container.SetViewMode(503)")
		elif opcao == '7': xbmc.executebuiltin("Container.SetViewMode(515)")

def setViewSeries() :
		xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')

		opcao = selfAddon.getSetting('seriesVisu')

		if   opcao == '0': xbmc.executebuiltin("Container.SetViewMode(50)")
		elif opcao == '1': xbmc.executebuiltin("Container.SetViewMode(51)")
		elif opcao == '2': xbmc.executebuiltin("Container.SetViewMode(500)")
		elif opcao == '3': xbmc.executebuiltin("Container.SetViewMode(501)")
		elif opcao == '4': xbmc.executebuiltin("Container.SetViewMode(508)")
		elif opcao == '5': xbmc.executebuiltin("Container.SetViewMode(504)")
		elif opcao == '6': xbmc.executebuiltin("Container.SetViewMode(503)")
		elif opcao == '7': xbmc.executebuiltin("Container.SetViewMode(515)")

def setViewTemporadas() :
		xbmcplugin.setContent(int(sys.argv[1]), 'seasons')

		opcao = selfAddon.getSetting('temporadasVisu')

		if   opcao == '0': xbmc.executebuiltin("Container.SetViewMode(50)")
		elif opcao == '1': xbmc.executebuiltin("Container.SetViewMode(51)")
		elif opcao == '2': xbmc.executebuiltin("Container.SetViewMode(500)")
		elif opcao == '3': xbmc.executebuiltin("Container.SetViewMode(501)")
		elif opcao == '4': xbmc.executebuiltin("Container.SetViewMode(508)")
		elif opcao == '5': xbmc.executebuiltin("Container.SetViewMode(504)")
		elif opcao == '6': xbmc.executebuiltin("Container.SetViewMode(503)")
		elif opcao == '7': xbmc.executebuiltin("Container.SetViewMode(515)")

def setViewEpisodios() :
		xbmcplugin.setContent(int(sys.argv[1]), 'seasons')

		opcao = selfAddon.getSetting('temporadasVisu')

		if   opcao == '0': xbmc.executebuiltin("Container.SetViewMode(50)")
		elif opcao == '1': xbmc.executebuiltin("Container.SetViewMode(51)")
		elif opcao == '2': xbmc.executebuiltin("Container.SetViewMode(500)")
		elif opcao == '3': xbmc.executebuiltin("Container.SetViewMode(501)")
		elif opcao == '4': xbmc.executebuiltin("Container.SetViewMode(508)")
		elif opcao == '5': xbmc.executebuiltin("Container.SetViewMode(504)")
		elif opcao == '6': xbmc.executebuiltin("Container.SetViewMode(503)")
		elif opcao == '7': xbmc.executebuiltin("Container.SetViewMode(515)")
		
def getRegexAll(text, start_with, end_with):
		r = re.findall("(?i)(" + start_with + "[\S\s]+?" + end_with + ")", text)
		
		return r

def getRegex(text, from_string, to_string, excluding=True):
		if excluding:
				try    : r = re.search("(?i)" + from_string + "([\S\s]+?)" + to_string, text).group(1)
				except : r = ''
		else:
				try    : r = re.search("(?i)(" + from_string + "[\S\s]+?" + to_string + ")", text).group(1)
				except : r = ''
				
		return r

############################################################################################################
              
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

try    : mode=int(params["mode"])
except : pass

try    : iconimage=urllib.unquote_plus(params["iconimage"])
except : pass

###############################################################################################################
#                                                   MODOS                                                     #
###############################################################################################################

if   mode == None : menuPrincipal()
elif mode == 10   : getCategorias(url)
elif mode == 20   : getFilmes(url)
elif mode == 40   : doPesquisa()
elif mode == 98   : getInfo(url)
elif mode == 99   : playTrailer(url)
elif mode == 100  : player(name,url,iconimage)
elif mode == 999  : openConfig()

xbmcplugin.endOfDirectory(int(sys.argv[1]))	




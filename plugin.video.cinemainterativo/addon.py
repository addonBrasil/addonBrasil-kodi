# -*- coding: UTF-8 -*-
#
# By AddonBrasil 08/12/2015
# Atualização 1.0.3: 29/12/2015
############################################################################################################

import urllib, urllib2, re, xbmcplugin, xbmcgui, xbmc, xbmcaddon, os, time
import urlresolver, urlparse

from resources.lib.BeautifulSoup import BeautifulSoup
from resources.lib               import client

addon_id    = 'plugin.video.cinemainterativo'
selfAddon   = xbmcaddon.Addon(id=addon_id)
datapath    = xbmc.translatePath(selfAddon.getAddonInfo('profile'))
addonfolder = selfAddon.getAddonInfo('path')
artfolder   = addonfolder + '/resources/img/'
icon        = addonfolder + '/icon.png'
fanart      = addonfolder + '/fanart.jpg'
base        = 'http://www.cinemainterativo.com'

############################################################################################################

def menuPrincipal():
		addDir('Categorias'                , base                  ,  10, artfolder + 'categorias.png')
		addDir('Últimos Filmes Adicionados', base                  ,  20, artfolder + 'ultimos.png')
		addDir('Filmes Dublados'           , base + '/?s=dublado'  ,  20, artfolder + 'filmes.png')
		addDir('Filmes Legendados'         , base + '/?s=legendado',  20, artfolder + 'filmes.png')
		addDir('Filmes por Ano'            , base                  ,  30, artfolder + 'filmes.png')
		addDir('Pesquisa de Filmes'        , '--'                  ,  40, artfolder + 'pesquisa.png')
		addDir('Configurações'             , base                  , 999, artfolder + 'config.png', 1, False)
			
		setViewMenu()	
		
def getCategorias(url):
		link  = openURL(url)
		soup  = BeautifulSoup(link)
		
		conteudo   = soup("div", {"class": "box-seletor"})
		categorias = conteudo[0]("option")
		
		totC = len(categorias)
		
		for categoria in categorias:
				titC = categoria.text.encode('utf-8', 'ignore')
				
				if not "Gênero" in titC :
						urlC = base + '/?cat=' + categoria["value"]
						imgC = artfolder + 'categorias.png'
						
						addDir(titC, urlC, 20, imgC)
				
		setViewMenu()		
		
def getFilmes(url):
		link  = openURL(url)
		soup  = BeautifulSoup(link)
		
		conteudo = soup("div", {"class": "row ultimos-filmes"})
		filmes   = conteudo[0]("div", {"class": "box-filme"})
		
		totF = len(filmes)
		
		for filme in filmes:
				titF = filme.h3.text.encode('utf-8', 'ignore')
				titF = titF.replace('Dublado - 1080p','').replace('Dublado - 720p','').replace('Legendado - 1080p','').replace('Legendado - 720p','')
				urlF = filme.a["href"]
				imgF = filme.img["src"].encode('utf-8', 'ignore')
				
				addDirF(titF, urlF, 100, imgF, False, totF)
				
		try : 
				proxima = re.findall('rel="next" href="(.*?)"', link)[0]
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
		mensagemprogresso = xbmcgui.DialogProgress()
		
		mensagemprogresso.create('CINEMA INTERATIVO', 'Obtendo fonte para ' + name, 'Por favor aguarde...')
		mensagemprogresso.update(0)
		
		link = openURL(url)
		
		vmID  = re.findall('".*?hashkey=(.*?)"', link)[0]
		urlVM = 'http://videomega.tv/view.php?ref=%s' % vmID
		
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
		
		xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
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
		#tracker.send("screenview", screenName="Config Screen")

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
		
def addDirF(name,url,mode,iconimage,pasta=True,total=1) :
		u  = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
		ok = True
		
		liz = xbmcgui.ListItem(name, iconImage="iconimage", thumbnailImage=iconimage)
		
		liz.setProperty('fanart_image', fanart)
		liz.setInfo(type="Video", infoLabels={"Title": name})
		
		cmItems = []
		
		cmItems.append(('[COLOR gold]Informações do Filme[/COLOR]', 'XBMC.RunPlugin(%s?url=%s&mode=98)'%(sys.argv[0], url)))
		cmItems.append(('[COLOR lime]Assistir Trailer[/COLOR]', 'XBMC.RunPlugin(%s?url=%s&mode=99)'%(sys.argv[0], urllib.quote_plus(url))))
		
		liz.addContextMenuItems(cmItems, replaceItems=False)
				
		ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
		
		return ok	
		
def getInfo(url)	:
		link = openURL(url)
		
		nomeF = re.findall('<span class="breadcrumb_last">(.*?)</span>', link)[0]
		
		try :
				nomeF = nomeF.split('&#8220;')[1]
				nomeF = nomeF.replace('&#8221;','')
		except :
				nomeF = nomeF.replace('Assistir ','').replace(' Online','')
				nomeF = nomeF.replace(' Dublado','').replace(' Legendado','').replace(' Nacional','')
				
		nomeF = nomeF.encode('utf-8', 'ignore').replace('&#8217;',"'").replace('&#038;','&')
		
		xbmc.executebuiltin('XBMC.RunScript(script.extendedinfo,info=extendedinfo,name=%s)' % nomeF)

def playTrailer(url):
		link = openURL(url)
		
		try :
				ytURL = re.findall('<iframe width="500" height="281" src="(.*?)" frameborder="0" allowfullscreen></iframe>', link)[0]
				ytURL = ytURL.replace('?feature=oembed','')
				ytID = ytURL.split('embed/')
				ytID = ytID[1]
		except :
				ytID = re.findall('<p>https://www.youtube.com/(.*?)</p>', link)[0]
				ytID = ytID.split('=')[1]
		
		xbmc.executebuiltin('XBMC.RunPlugin("plugin://script.extendedinfo/?info=youtubevideo&&id=%s")' % ytID)
	
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
elif mode == 30   : getAnos(url)
elif mode == 40   : doPesquisa()
elif mode == 98   : getInfo(url)
elif mode == 99   : playTrailer(url)
elif mode == 100  : player(name,url,iconimage)
elif mode == 999  : openConfig()

xbmcplugin.endOfDirectory(int(sys.argv[1]))	
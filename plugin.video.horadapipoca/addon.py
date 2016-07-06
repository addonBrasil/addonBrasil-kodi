#####################################################################
# -*- coding: utf-8 -*-
#####################################################################
# Addon : Hora Da Pipoca
# By AddonBrasil - 11/12/2015
# Atualizado (1.0.1) - 15/12/2015
# Atualizado (1.1.0) - 12/03/2016
#####################################################################

import urllib, urllib2, re, xbmcplugin, xbmcgui, xbmc, xbmcaddon, os, time, base64
import urlresolver

from resources.lib.BeautifulSoup import BeautifulSoup
from resources.lib               import jsunpack

addon_id  = 'plugin.video.horadapipoca'
selfAddon = xbmcaddon.Addon(id=addon_id)

addonfolder = selfAddon.getAddonInfo('path')
artfolder   = addonfolder + '/resources/img/'
fanart      = addonfolder + '/fanart.jpg'
base        = base64.b64decode('aHR0cDovL2VmaWxtZXNuYXJlZGUuY29t')

############################################################################################################

def menuPrincipal():
		addDir('Categorias'                , base                            ,   10, artfolder + 'categorias.png')
		addDir('Lançamentos'               , base + '/category/lancamentos/' ,   20, artfolder + 'lancamentos.png')
		addDir('Legendados'                , base + '/category/legendados/'  ,   20, artfolder + 'legendados.png')
		addDir('HD 720p'                   , base + '/category/blu-ray-720p/',   20, artfolder + 'hd720p.png')
		addDir('Pesquisa'                  , '--'                            ,   30, artfolder + 'pesquisa.png')
		addDir('Configurações'             , base                            ,  999, artfolder + 'config.png', 1, False)
		addDir('Configurações ExtendedInfo', base                            , 1000, artfolder + 'config.png', 1, False)
			
		setViewMenu()		
		
def getCategorias(url):
		link = openURL(url)
		soup = BeautifulSoup(link)
		
		conteudo   = soup("ul", {"class": "m-cat"})
		
		categorias = conteudo[0]("li")
				
		totC = len(categorias)
		
		for categoria in categorias:
				titC = categoria.text.encode('latin-1','replace')
				
				if not 'Lançamento' in titC :
						urlC = categoria.a["href"]
						imgC = artfolder + limpa(titC) + '.png'
				
						addDir(titC,urlC,20,imgC)
			
		setViewMenu()		
		
def getFilmes(url):
		link  = openURL(url)
		link = unicode(link, 'utf-8', 'ignore')		
		
		soup     = BeautifulSoup(link)
		conteudo = soup("div", {"class": "ib-miniaturas lista-miniaturas"})
		filmes   = conteudo[0]("div", {"class": "ib-miniatura"})
		
		totF = len(filmes)
		
		for filme in filmes:
				titF = filme.img["alt"].encode('utf-8', 'ignore')
				titF = titF.replace('Assistir ','').replace('Filme ','')
				urlF = filme.a["href"].encode('utf-8', 'ignore')
				imgF = filme.img["src"].encode('utf-8', 'ignore')
				
				addDirF(titF, urlF, 100, imgF, False, totF)
				
		try : 
				proxima = re.findall('link rel="next" href="(.*?)"', link)[0]
				addDir('Próxima Página >>', proxima, 20, artfolder + 'proxima.png')
		except : 
				pass
				
		setViewFilmes()

def doPesquisa():
		keyb = xbmc.Keyboard('', 'Pesquisar Filmes')
		keyb.doModal()

		if (keyb.isConfirmed()):
				texto    = keyb.getText()
				pesquisa = urllib.quote(texto)
				url      = base + '?s=%s' % str(pesquisa)
				
				getFilmes(url)
				
def player(name,url,iconimage):
		OK = True
		mensagemprogresso = xbmcgui.DialogProgress()
		mensagemprogresso.create('HORA DA PIPOCA', 'Obtendo Fontes para ' + name, 'Por favor aguarde...')
		mensagemprogresso.update(0)
		
		titsT = []
		idsT = []
		
		matriz = []
		
		link = openURL(url)
		soup  = BeautifulSoup(link)
		
		try :
				conteudo = soup("div", {"class": "pn-opcoes pn-dub"})
				srvsdub  = conteudo[0]("li")
		
				totD = len(srvsdub)

				tipo = "Dublado"

				for i in range(totD) :
						titS = srvsdub[i].text.encode('utf-8','ignore') + " (%s)" % tipo
						
						if not 'Principal' in titS :
								if not 'DropVideo' in titS :
									if not 'Vídeo PW' in titS :
										if not 'YouWatch' in titS :
											if not 'Youwatch' in titS :
													if not 'NeoDrive' in titS :
															idS = srvsdub[i]["data-pid"]
															titsT.append(titS)
															idsT.append(idS)
		except :
				pass
				
		try :
				conteudo = soup("div", {"class": "pn-opcoes pn-leg"})
				srvsleg  = conteudo[0]("li")

				totL = len(srvsleg)
				
				tipo = "Legendado"

				for i in range(totL) :
						titS = srvsleg[i].text.encode('utf-8','ignore') + " (%s)" % tipo
						
						if not 'Principal' in titS :
								if not 'DropVideo' in titS :
									if not 'Vídeo PW' in titS :
										if not 'YouWatch' in titS :
											if not 'Youwatch' in titS :
													if not 'NeoDrive' in titS :
															idS = srvsleg[i]["data-pid"]
															titsT.append(titS)
															idsT.append(idS)
		except :
				pass
		
		if not titsT : return
		
		index = xbmcgui.Dialog().select('Selecione uma das fontes suportadas :', titsT)
		
		if index == -1 : return
		
		ind = idsT[index]
		
		conteudo = soup("li", {"class": "pi-item"+ind})
		
		links = conteudo[0]("iframe")
		
		if len(links) == 0 : links = conteudo[0]("embed")
		
		for link in links :
				urlVideo = link["data-src"]
		
		print "URLVIDEO " + urlVideo
		
		mensagemprogresso.update(50, 'Resolvendo fonte para ' + name,'Por favor aguarde...')
				
		if 'nowvideo.php' in urlVideo :
				nowID = urlVideo.split("id=")[1]
				urlVideo = 'http://embed.nowvideo.sx/embed.php?v=%s' % nowID
				
		elif 'video.tt' in urlVideo :
				vttID = urlVideo.split('e/')[1]
				urlVideo = 'http://www.video.tt/watch_video.php?v=%s' % vttID
				
		elif 'flashx.php' in urlVideo :
				fxID = urlVideo.split('id=')[1]
				urlVideo = 'http://www.flashx.tv/embed-%s.html' % fxID
				
		elif 'thevid.net' in urlVideo :
				linkTV = openURL(urlVideo)
				js_data = jsunpack.unpack(linkTV)
				
				url2Play = re.findall('var vurl2="(.*?)"', js_data)[0]
				
				OK = False
				
		if OK : url2Play = urlresolver.resolve(urlVideo)

		if not url2Play : return
		
		legendas = '-'
		
		mensagemprogresso.update(75, 'Abrindo Sinal para ' + name,'Por favor aguarde...')
		
		playlist = xbmc.PlayList(1)
		playlist.clear()
		
		listitem = xbmcgui.ListItem(name,thumbnailImage=iconimage) 
		listitem.setPath(url2Play)
		listitem.setProperty('mimetype','video/mp4')
		listitem.setProperty('IsPlayable', 'true')
		playlist.add(url2Play,listitem)

		xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
		xbmcPlayer.play(playlist)
		
		mensagemprogresso.update(100)
		mensagemprogresso.close()
		
		if legendas != '-':
			if 'timedtext' in legendas:
					import os.path
					sfile = os.path.join(xbmc.translatePath("special://temp"),'sub.srt')
					sfile_xml = os.path.join(xbmc.translatePath("special://temp"),'sub.xml')#timedtext
					sub_file_xml = open(sfile_xml,'w')
					sub_file_xml.write(urllib2.urlopen(legendas).read())
					sub_file_xml.close()
					xmltosrt.main(sfile_xml)
					xbmcPlayer.setSubtitles(sfile)
			else:
				xbmcPlayer.setSubtitles(legendas)
				
############################################################################################################
		
def openConfig():
		selfAddon.openSettings()
		setViewMenu()
		xbmcplugin.endOfDirectory(int(sys.argv[1]))
		
def openConfigEI():
		eiID  = 'script.extendedinfo'
		eiAD  = xbmcaddon.Addon(id=eiID)

		eiAD.openSettings()
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
		cmItems.append(('[COLOR red]Assistir Trailer[/COLOR]', 'XBMC.RunPlugin(%s?name=%s&url=%s&iconimage=%s&mode=99)'%(sys.argv[0], urllib.quote(name), url, urllib.quote(iconimage))))
		
		liz.addContextMenuItems(cmItems, replaceItems=False)
				
		ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
		
		return ok	

def getInfo(url)	:
		link = openURL(url)
		titO = re.findall('<li>Titulo original: <span>(.*?)</span></li>', link)[0]
				
		xbmc.executebuiltin('XBMC.RunScript(script.extendedinfo,info=extendedinfo, name=%s)' % titO)

def playTrailer(name, url,iconimage):
		link = openURL(url)
		ytID = re.findall('<iframe width=".*?" height=".*?" src="http://www.youtube.com/embed/(.*?)" frameborder="0" allowfullscreen></iframe>', link)[0]
		
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
		
def limpa(texto):
		texto = texto.replace('ç','c').replace('ã','a').replace('õ','o')
		texto = texto.replace('â','a').replace('ê','e').replace('ô','o')
		texto = texto.replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u')
		texto = texto.replace(' ','-')
		texto = texto.lower()
		
		return texto
		
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

try    : url=urllib.unquote_plus(params["url"])
except : pass
try    : name=urllib.unquote_plus(params["name"])
except : pass
try    : mode=int(params["mode"])
except : pass
try    : iconimage=urllib.unquote_plus(params["iconimage"])
except : pass

#print "Mode: "+str(mode)
#print "URL: "+str(url)
#print "Name: "+str(name)
#print "Iconimage: "+str(iconimage)

###############################################################################################################

if   mode == None : menuPrincipal()
elif mode == 10   : getCategorias(url)
elif mode == 20   : getFilmes(url)
elif mode == 30   : doPesquisa()
elif mode == 40   : getFavoritos()
elif mode == 41   : addFavoritos(name,url,iconimage)
elif mode == 42   : remFavoritos(name,url,iconimage)
elif mode == 43   : cleanFavoritos()
elif mode == 98   : getInfo(url)
elif mode == 99   : playTrailer(name,url,iconimage)
elif mode == 100  : player(name,url,iconimage)
elif mode == 999  : openConfig()
elif mode == 1000 : openConfigEI()

xbmcplugin.endOfDirectory(int(sys.argv[1]))	
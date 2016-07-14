#####################################################################
# -*- coding: utf-8 -*-
# Addon : Arquivo Brasil
# By AddonBrasil     - 28/07/2015
# Atualizado (1.3.6) - 22/12/2015
# Atualizado (1.3.7) - 14/01/2016
# Atualizado (1.3.8) - 14/07/2016
#####################################################################

import urllib,urllib2,re,xbmcplugin, xbmcaddon, xbmcgui, time, base64
import urlresolver

from resources.lib import client
from resources.lib import jsunpack
from resources.lib.BeautifulSoup import BeautifulSoup
from resources.lib.UniversalAnalytics import Tracker

addon_id    = 'plugin.video.arquivobrasil'
selfAddon   = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')

icon    = addonfolder + '/icon.png'
fanart  = addonfolder + '/fanart.jpg'

base   = base64.b64decode('aHR0cDovL25vdmVsYXNncmF2YWRhcy5uZXQv')
basex  = base64.b64decode('aHR0cDovL3Rhbm9hci50di8=')

imgsrv = base64.b64decode('aHR0cDovL2FycXVpdm9icmFzaWwuYWRkb25icmFzaWwudGsvaW1ncy8=')

agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'

ga = {
	"enabled"    : False,
	"UA"         : 'UA-67989726-3',
	"appName"    : selfAddon.getAddonInfo("name"),
	"appVersion" : selfAddon.getAddonInfo("version"),
	"appId"      : selfAddon.getAddonInfo("id")
}

tracker = Tracker.create(ga["UA"]);
tracker.set("appName", ga["appName"]);
tracker.set("appVersion", ga["appVersion"]);
tracker.set("appId", ga["appId"]);

ga["enabled"] = True;

if (selfAddon.getSetting("uuid") == ""):
		selfAddon.setSetting("uuid", tracker.params["cid"]);
else:
		tracker.set("clientId", selfAddon.getSetting("uuid"));
	
#####################################################################

def menuPrincipal():
		addDir('Novelas'      , base,  10, imgsrv + 'novelas.jpg')
		addDir('Séries'       , base,  10, imgsrv + 'series.jpg')
		addDir('Jornalismo'   , base,  10, imgsrv + 'jornalismo.jpg')
		addDir('Variedades'   , base,  10, imgsrv + 'variedades.jpg')
		addDir('Esportes'     , base,  10, imgsrv + 'esportes.jpg')
		#addDir('Extras'       , base,  30, imgsrv + 'extras.jpg')
		addDir('Configurações', base, 999, imgsrv + 'config.jpg', False)

		setViewMenu()
		
def menuExtras():
		addDir('Malhação 2015'    , basex + '?novos=1&e=malhacao-2015'                , 40, imgsrv + 'malhacao.png')
		addDir('Hora 1 da Notícia', basex + '?novos=1&e=hora-1'                       , 40, imgsrv + 'hora-1.png')
		addDir('Jornal Hoje'      , basex + '?novos=1&e=jornal-hoje'                  , 40, imgsrv + 'jornal-hoje.png')
		addDir('Bem Estar'        , basex + '?novos=1&e=bem-estar'                    , 40, imgsrv + 'bem-estar.png')
		addDir('CQC'              , basex + '?novos=1&e=cqc'                          , 40, imgsrv + 'cqc.png')
		addDir('É de Casa'        , basex + '?novos=1&e=e-de-casa'                    , 40, imgsrv + 'e-de-casa.png')
		addDir('Encontro'         , basex + '?novos=1&e=encontro-com-fatima-bernardes', 40, imgsrv + 'encontro.png')
		addDir('Esquenta'         , basex + '?novos=1&e=esquenta'                     , 40, imgsrv + 'esquenta.png')
		addDir('Estrelas'         , basex + '?novos=1&e=estrelas'                     , 40, imgsrv + 'estrelas.png')
		addDir('Mais Você'        , basex + '?novos=1&e=mais-voce'                    , 40, imgsrv + 'mais-voce.png')
		addDir('Programa do Gugu' , basex + '?novos=1&e=programa-do-gugu'             , 40, imgsrv + 'gugu.png')
		addDir('Programa Raul Gil', basex + '?novos=1&e=programa-raul-gil'            , 40, imgsrv + 'raul-gil.png')
		addDir('Video Show'       , basex + '?novos=1&e=video-show'                   , 40, imgsrv + 'video-show.png')
		
		tracker.send("screenview", screenName="Menu Extras")
		
		setViewMenu()
		
def getListaCat(url, name):
		link = openURL(url)
		soup = BeautifulSoup(link)
		conteudo = soup("div", {"id": "navigation"})
		
		listaGeral = conteudo[0]("ul", {"class": "sub-menu"} )
		
		if   name == 'Novelas'    : temp = listaGeral[0]
		elif name == 'Séries'     : temp = listaGeral[1]
		elif name == 'Jornalismo' : temp = listaGeral[2]
		elif name == 'Variedades' : temp = listaGeral[3]
		elif name == 'Esportes'   : temp = listaGeral[4]
		elif name == 'Extras'     : menuExtras()
		
		categorias = temp("li")
		
		totCategorias = len(categorias)
		
		for categoria in categorias:
				titcat = categoria.text.replace('&#038;','&').encode('utf-8', 'ignore')
				urlcat = categoria.a["href"]
				imgcat = imgsrv + getImg(titcat)
				
				addDir(titcat, urlcat, 20, imgcat, totCategorias, True)		

		tracker.send("screenview", screenName="Listagem da Categoria - " + name)

		setViewMenu()
		
def getVideosCat(url, name, iconimage):
		link  = openURL(url)
		soup  = BeautifulSoup(link)
		
		conteudo = soup("div", {"class": "block archive"})
		videos   = conteudo[0]("div", {"class": "block-image"})
		
		totVideos = len(videos)
		
		for video in videos:
				url = video.a["href"]
				tit = video.img["alt"].replace('&#038;','&').replace('&#8211;',"-").replace(' de ',' - ').replace(' Completo','').replace('feira,','feira').encode('utf-8', 'ignore')
				img = video.img["src"] 
				addDir(tit, url, 100, img, False, totVideos)
				
		try :
				paginas = re.compile("<span class='current'>.*?</span><a href='(.*?)' class='inactive' >.*?</a>").findall(link)
				
				for proxpag in paginas:
						addDir('Próxima Página >>', proxpag, 20, imgsrv + 'proxima.jpg')
						break
		except :
				pass
				
		tracker.send("screenview", screenName="Lista de Videos Categoria - "+ name)
				
		setViewVideos()
		
def getVideosExt(url, name, iconimage):
		link  = openURL(url)
		soup  = BeautifulSoup(link)
		
		titulos = re.compile("title='(.*?)'").findall(link)
		urls    = re.compile("Loadn\('(.*?)&").findall(link)
		imgs    = re.compile("image:url\((.*?)\)").findall(link)
		
		i = 0
		
		for i in range(0,len(titulos)):
			titE = titulos[i]
			
			urlE = basex + str(urls[i])
			imgE = imgs[i]
			
			addDir(titE, urlE, 200, imgE, False)
				
		try :
				paginas = re.compile('<b>.*?</b>, <a style=cursor:pointer onclick=Loadn\("(.*?)"').findall(link)
				
				for proxpag in paginas:
						addDir('Próxima Página >>', basex + proxpag, 20, imgsrv + 'proxima.jpg')
						break
		except :
				pass
				
		tracker.send("screenview", screenName="Listagem de Videos Extras - "+ name)
				
		setViewVideos()
		
def doPlay(url, name):
		link = openURL(url)
		
		pg = 0
		msgDialog = xbmcgui.DialogProgress()

		msgDialog.create('ARQUIVO BRASIL', 'Abrindo Sinal', name, 'Por favor aguarde...')
		msgDialog.update(25)
		
		playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
		playlist.clear()

		msgDialog.update(50)
		
		OK = True
		
		try :
				url2Rslv = re.findall('<IFRAME SRC="(.*?)" FRAMEBORDER=0 MARGINWIDTH=0 MARGINHEIGHT=0 SCROLLING=NO WIDTH=645 HEIGHT=355></IFRAME>', link)[0]
				url2Rslv = url2Rslv.replace('embed-','')
				url2Play = getURL2Play(url2Rslv)
				needPlaylist = False
		except :
				try :
						url2Rslv = re.findall('<iframe width="645" height="355" scrolling="no" frameborder="0" src="(.*?)" allowFullScreen></iframe></p>', link)[0]
						url2Play = urlresolver.resolve(url2Rslv)
						url2Play = url2Play + ' |User-agent:' + agent
						needPlaylist = False
				except :
						try : 
								url2Rslv = re.findall('<iframe width="645" height="355" src="(.*?)"', link)[0]
								url2Play = urlresolver.resolve(url2Rslv)
								url2Play = url2Play + ' |User-agent:' + agent
								needPlaylist = False
						except :
								try :
										url2Rslv = re.findall('flashvars="&#038;file=(.*?)&#038;skin', link)[0]
										linkRslv = openURL(url2Rslv)
										url2Play = re.findall('<location>(.*?)</location>', linkRslv)
										totu2p = len(url2Play)
										needPlaylist = True
								except :
										try :
												url2Rslv = re.findall('<iframe src="(.*?)" scrolling="no" frameborder="0" width="100%" height="355" allowfullscreen="true" webkitallowfullscreen="true" mozallowfullscreen="true"></iframe></p>', link)[0]
												url2Play = urlresolver.resolve(url2Rslv)
												url2Play = url2Play + ' |User-agent:' + agent
												needPlaylist = False
										except :
												msgDialog.update(100)
												dialog = xbmcgui.Dialog()
												dialog.ok("ARQUIVO BRASIL", "Servidor não Suportado", "Este vídeo não pode ser executado devido ao servidor não ser suportado...", "Pedimos desculpas pelo transtorno.")		
												OK = False
										
		if OK :
				msgDialog.update(75)

				playlist = xbmc.PlayList(1)
				playlist.clear()
				
				if url2Play :
						if needPlaylist:
								for i in range(0,totu2p) :
										urlFinal = url2Play[i]
										
										if 'youtube' in urlFinal :
												ytID = urlFinal.partition('v=')
												ytID = ytID[2]
												
												urlFinal = 'plugin://plugin.video.youtube/play/?video_id=' + str(ytID)

										liz = xbmcgui.ListItem(name, thumbnailImage=iconimage)
										liz.setInfo('video', {'Title': name})
										liz.setPath(urlFinal)
										liz.setProperty('mimetype','video/mp4')
										liz.setProperty('IsPlayable', 'true')
										playlist.add(urlFinal, liz)
						else :
								liz = xbmcgui.ListItem(name, thumbnailImage=iconimage)
								liz.setInfo('video', {'Title': name})
								liz.setPath(url2Play)
								liz.setProperty('mimetype','video/mp4')
								liz.setProperty('IsPlayable', 'true')
								playlist.add(url2Play, liz)
										
						msgDialog.update(100)
						
						tracker.send("event", "Usage", "Play Video - " + name, "video", screenName="Play Screen");
						
						xbmc.Player().play(playlist,liz)
				else:
						msgDialog.update(100)
						dialog = xbmcgui.Dialog()
						dialog.ok("ARQUIVO BRASIL", "Vídeo Indisponível", "Este vídeo ainda não esta disponível...", "Tente novamente em breve.")		
				
def doPlayExt(url, name):
		link = openURL(url)

		pg = 0
		msgDialog = xbmcgui.DialogProgress()

		msgDialog.create('ARQUIVO BRASIL', 'Abrindo Sinal', name, 'Por favor aguarde...')
		msgDialog.update(25)
		
		playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
		playlist.clear()

		urlExt = re.findall("<iframe src='(.*?)'", link)[0]
		
		linkExt = openURL(urlExt)
		
		msgDialog.update(50)
		
		if 'dailymotion' in linkExt :
				urlDM = re.findall("src='http://www.dailymotion.com/(.*?)'", linkExt)[0]
				urlDM = 'http://www.dailymotion.com/' + str(urlDM)

				url2Play = getDmURL(urlDM)
		else :
				urlRSS   = urlExt + '.rss'
				linkRSS  = openURL(urlRSS)
				url2Play = re.findall('<jwplayer:source file="(.*?)" />', linkRSS)		
		
		msgDialog.update(75)
		
		if url2Play:
					liz = xbmcgui.ListItem(name, thumbnailImage=iconimage)
					liz.setInfo('video', {'Title': name})
					
					if 'dailymotion' in url2Play :
							liz.setPath(url2Play)
							liz.setProperty('mimetype','video/mp4')
							liz.setProperty('IsPlayable', 'true')
							
							playlist.add(url=url2Play, listitem=liz, index=7)
					else :
							
							i = 0
							
							for i in range(len(url2Play)) :
									urls2Play = url2Play[i].replace('./','http://dnshost.cf/player1/' )
									
									liz = xbmcgui.ListItem(name, thumbnailImage=iconimage)
									
									liz.setInfo('video', {'Title': name})
									liz.setPath(urls2Play)
									liz.setProperty('mimetype','video/mp4')
									liz.setProperty('IsPlayable', 'true')
									
									playlist.add(urls2Play, liz)
									
									i+=1
						
					msgDialog.update(100)
					
					tracker.send("event", "Usage", "Play Video Extra - " + name, "video", screenName="Play Screen Extra");
				
					xbmc.Player(xbmc.PLAYER_CORE_AUTO).play(playlist)
		else:
				msgDialog.update(100)
				dialog = xbmcgui.Dialog()
				dialog.ok("ARQUIVO BRASIL", "Vídeo Indisponível", "Este vídeo ainda não esta disponível...", "Tente novamente em breve.")		
		
def getURL2Play(url):
    try:
        result = client.request(url, mobile=True, close=False)

        try:
            post = {}
						
            f = client.parseDOM(result, 'Form', attrs = {'method': 'POST'})[0]
            f = f.replace('"submit"', '"hidden"')
						
            k = client.parseDOM(f, 'input', ret='name', attrs = {'type': 'hidden'})
						
            for i in k: 
								post.update({i: client.parseDOM(f, 'input', ret='value', attrs = {'name': i})[0]})
								
            post = urllib.urlencode(post)
        except:
            post = None

        for i in range(0, 10):
            try:
                result = client.request(url, post=post, mobile=True, close=False)
                result = result.replace('\n','')

                result = re.compile('(eval.*?\)\)\))').findall(result)[-1]
                result = jsunpack.unpack(result)

                result = re.compile('sources *: *\[.+?\]').findall(result)[-1]
                result = re.compile('file *: *"(http.+?)"').findall(result)

                url = [i for i in result if '.m3u8' in i]
								
                if len(url) > 0: return url[0]
            except:
                time.sleep(1)
    except:
        return
				
def getDmURL(vURL) :
		urlVideo = urlresolver.resolve(vURL)
		
		if urlVideo : return urlVideo
		else        : return ''
		
def getImg(texto):
		texto = texto.lower()
		texto = texto.replace('ç','c').replace('ã','a').replace('õ','o')
		texto = texto.replace('â','a').replace('ê','e').replace('ô','o')
		texto = texto.replace('á','a').replace('é','e').replace('í','i').replace('Í','i').replace('ó','o').replace('ú','u').replace('ü','u')
		texto = texto.replace('&','').replace(' ', '-').replace('.', '-').replace(',', '-').replace('--','-')
		texto = texto + '.png'
		return texto
		
def openConfig():
		selfAddon.openSettings()

		tracker.send("screenview", screenName="Configurações")
		
		setViewMenu()
		
		xbmcplugin.endOfDirectory(int(sys.argv[1]))

def setViewMenu() :
		xbmcplugin.setContent(int(sys.argv[1]), 'movies')
		
		opcao = selfAddon.getSetting('menuVisu')
		
		if   opcao == '0': xbmc.executebuiltin("Container.SetViewMode(50)")
		elif opcao == '1': xbmc.executebuiltin("Container.SetViewMode(51)")
		elif opcao == '2': xbmc.executebuiltin("Container.SetViewMode(500)")
		
def setViewVideos() :
		xbmcplugin.setContent(int(sys.argv[1]), 'episodes')

		opcao = selfAddon.getSetting('videosVisu')

		if   opcao == '0': xbmc.executebuiltin("Container.SetViewMode(50)")
		elif opcao == '1': xbmc.executebuiltin("Container.SetViewMode(51)")
		elif opcao == '2': xbmc.executebuiltin("Container.SetViewMode(500)")

def openURL(url):
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = urllib2.urlopen(req)
		link = response.read()
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

#print "Mode : " + str(mode)
#print "Icon : " + str(iconimage)
#print "URL  : " + str(url)
#print "Name : " + str(name)

#####################################################################

if mode == None : 
		try : 
				Tracker
		except NameError:
				from UniversalAnalytics import Tracker;
				tracker = Tracker.create(ga["UA"]);
				tracker.set("appName", ga["appName"]);
				tracker.set("appVersion", ga["appVersion"]);
				tracker.set("appId", ga["appId"]);
				
				if (selfAddon.getSetting("uuid") == ""):
					selfAddon.setSetting("uuid", tracker.params["cid"]);
				else:
					tracker.set("clientId", selfAddon.getSetting("uuid"));
			
		tracker.send("event", "Usage", "install", screenName="Menu Principal")

		menuPrincipal()
		
elif mode == 10  : getListaCat(url, name)
elif mode == 20  : getVideosCat(url, name, iconimage)
elif mode == 30  : menuExtras()
elif mode == 40  : getVideosExt(url, name, iconimage)
elif mode == 100 : doPlay(url, name)
elif mode == 200 : doPlayExt(url, name)
elif mode == 999 : openConfig()

	
xbmcplugin.endOfDirectory(int(sys.argv[1]))
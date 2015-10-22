# -*- coding: utf-8 -*-
#
# 21/10/2015 - By AddonBrasil
###############################################################################

import xbmc,xbmcaddon,xbmcgui,xbmcplugin,urllib,urllib2,os,re,sys,datetime,time
from plugintools import *

###############################################################################

addon_id    = 'plugin.video.ei'
selfAddon   = xbmcaddon.Addon(id=addon_id)
datapath    = xbmc.translatePath(selfAddon.getAddonInfo('profile'))
addonfolder = selfAddon.getAddonInfo('path')

icon    = addonfolder + '/icon.png'
fanart  = addonfolder + '/fanart.jpg'
base    = 'http://ei.addonbrasil.tk/'
baseprg = 'http://www.vcfaz.tv/programacao.php?canal='
###############################################################################

def menu(url):
		link = openURL(url)
		
		menu = re.compile('<name>(.+?)</name>.+?<mode>(.+?)</mode>.+?<thumbnail>(.+?)</thumbnail>.+?<fanart>(.+?)</fanart>.+?<link>(.+?)</link>',re.DOTALL).findall(link)
		
		for name , mode, iconimage ,fanart, url in menu:
				addDir(name, url, mode, iconimage, fanart)
				
		addDir('Configurações', base, 999, base + 'imgs/icons/configuracoes.png', fanart, False)
				
		setViewMenu()
		
def menuLive(url):	
		link = openURL(url)
		
		if '<item>' in link : 
				items = link.split('<item>')
				
				for item in items:
						if len(item) > 1 :
								info  = re.compile('<title epg="(.*?)">(.*?)</title>').findall(item)[0]
								nameL = info[1]
								idL   = info[0]
								imgL  = re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]
								item  = item.replace('\n','')
								urlL  = re.compile('<link>(.+?)</link>').findall(item)[0]
								
								addDir2(nameL, urlL, 100, imgL, fanart, idL)
								
		setViewMenu()

def menuVod():
		params = get_params()
		action = params.get("action")
		
		if params.get("action") is None: 
				add_item(title = "Esporte Interativo", 
									url = "plugin://plugin.video.youtube/user/videosei/", 
									thumbnail = base + 'imgs/icons/videosei.png', 
									folder = True )
				add_item(title = "Esporte Interativo NE", 
									url = "plugin://plugin.video.youtube/user/einordeste/", 
									thumbnail = base + 'imgs/icons/eine.png', 
									folder = True )
				add_item(title = "Esporte Interativo 24h", 
									url = "plugin://plugin.video.youtube/user/esporteinterativo24h/", 
									thumbnail = base + 'imgs/icons/ei24h.png', 
									folder = True )
		else:
				action = params.get("action")
				exec action+"(params)"
				
		close_item_list()
		
		setViewMenu()
		
def playLive(url, name, iconimage) :
		titVideo = name
		
		if 'sublink' in url:
				match = re.compile('<sublink name="(.*?)">(.*?)</sublink>').findall(url)
				
				names = []
				urls  = []
				
				for NAME, URL in match:
						names.append(NAME)
						urls.append(str(URL))
								
				opcao = xbmcgui.Dialog().select('Selecione a resolução desejada :', names)

				if opcao == -1 : return

				url = urls[opcao]
				
				titulo = name + ' - ' + names[opcao]
				
		playlist = xbmc.PlayList(1)
		playlist.clear()
		
		liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
		
		liz.setInfo("Video", {"Title":titulo, "overlay":6, "playcount":0})
		liz.setProperty('IsPlayable', 'true')
		
		playlist.add(url, liz)
		
		xbmcplugin.setResolvedUrl(int(sys.argv[1]),True,liz)

		if int(sys.argv[1]) < 0 : xbmc.Player().play(playlist,liz)
		
def getProgramacao(idcanal, name):
		url  = baseprg + str(idcanal)
		link = openURL(url)
		
		datatit   = re.compile("canal=.*?&data=.*?';\">(.*?)</option> ").findall(link)[0]
		titulos   = ['[B][COLOR blue]%s[/COLOR][/B]' % datatit]
		programas = re.compile("hora=(.*?)' class='outros'><b>(.*?)</b></a></span><br /><span class='stylehora2'>(.*?) <img").findall(link)
		
		ref = 0

		for horaP, nomeP, tipoP in programas:
				ref += 1
				titulos.append('\n[B][COLOR red]%s [/COLOR][/B] - [B][COLOR white]%s[/COLOR] [COLOR gold](%s)[/COLOR][/B]' % (horaP, nomeP, tipoP))			
				
		programacao = '\n'.join(titulos)
		
		try:
				xbmc.executebuiltin("ActivateWindow(10147)")
				window = xbmcgui.Window(10147)
				xbmc.sleep(100)
				
				canal = name.partition(' - ')
				
				canalProg = canal[0]
				canalProg.replace('[B]','').replace('[/B]','')
				
				window.getControl(1).setLabel('Programação para o canal %s' % str(canalProg))
				window.getControl(5).setText(programacao)
		except: 
				pass
				
def openConfig():
		selfAddon.openSettings()
		setViewMenu()
		xbmcplugin.endOfDirectory(int(sys.argv[1]))

def setViewMenu() :
		xbmcplugin.setContent(int(sys.argv[1]), 'movies')
		
		opcao = selfAddon.getSetting('visu')
		
		if   opcao == '0': xbmc.executebuiltin("Container.SetViewMode(50)")
		elif opcao == '1': xbmc.executebuiltin("Container.SetViewMode(51)")
		elif opcao == '2': xbmc.executebuiltin("Container.SetViewMode(500)")
		
def openURL(url):
		req = urllib2.Request(url)
		req.add_header('User-Agent' , "Magic Browser")
		response = urllib2.urlopen(req)
		link = response.read()
		response.close()
		
		return link
		
def addLink(name, url, iconimage, fanart):
		liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
		liz.setInfo( type="Video", infoLabels={ "Title": name } )
		liz.setProperty("IsPlayable","true")
		liz.setProperty("Fanart_Image", fanart )
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
		
def addDir(name,url,mode,iconimage,fanart,pasta=True,total=1):
		u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
		ok=True
		liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
		liz.setProperty('fanart_image', fanart)
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
		return ok

def addDir2(name, url, mode, iconimage, fanart, idcanal):
		u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&idcanal="+urllib.quote_plus(idcanal)
		
		ok = True

		liz=xbmcgui.ListItem(name, iconImage="iconimage", thumbnailImage=iconimage)
		liz.setInfo( type="Video", infoLabels={"Title": name})
		liz.setProperty('fanart_image', fanart)
				
		cm = []
		cm.append(('Grade de Programação [B][COLOR red](Beta)[/COLOR][/B]', "XBMC.RunPlugin(%s?mode=%s&idcanal=%s&name=%s)"%(sys.argv[0],90,idcanal,name)))

		liz.addContextMenuItems(cm, replaceItems=False)

		if mode == 100 :
				liz.setProperty("IsPlayable","true")
				ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
		else:
				ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
				
		return ok

def setView(content, viewType):
    if content : 
				xbmcplugin.setContent(int(sys.argv[1]), content)
    if selfAddon.getSetting('auto-view')=='true' : 
				xbmc.executebuiltin("Container.SetViewMode(%s)" % selfAddon.getSetting(viewType) )

###############################################################################

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
mode      = None
iconimage = None
url       = None
name      = None
idcanal   = None

try    : mode = int(params["mode"])
except : pass
try    : iconimage = urllib.unquote_plus(params["iconimage"])
except : pass
try    : url = urllib.unquote_plus(params["url"])
except : pass
try    : name = urllib.unquote_plus(params["name"])
except : pass
try    : idcanal = urllib.unquote_plus(params["idcanal"])
except : pass

###############################################################################

#print "Mode    : " + str(mode)
#print "Icon    : " + str(iconimage)
#print "URL     : " + str(url)
#print "Name    : " + str(name)
#print "IDCanal : " + str(idcanal)

if   mode == None : menu(url=base+'?x=menu') 
elif mode == 10   : menu(url)
elif mode == 20   : menuLive(url)
elif mode == 30   : menuVod()
elif mode == 90   : getProgramacao(idcanal, name)
elif mode == 100  : playLive(url, name, iconimage)
elif mode == 999  : openConfig()

xbmcplugin.endOfDirectory(int(sys.argv[1]))

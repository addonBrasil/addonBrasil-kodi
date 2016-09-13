#!/usr/bin/python
# -*- coding: utf-8 -*-
###########################################################
import xbmcplugin, xbmcgui, xbmcaddon, xbmcvfs, os, re, sys
import urllib, urllib2, datetime, time
import json, shutil, random, socket

from operator import itemgetter
from datetime import date

addonID = 'plugin.video.itunestube'
addon   = xbmcaddon.Addon(id=addonID)

icon    = xbmc.translatePath('special://home/addons/'+addonID+'/icon.png')
fanart  = xbmc.translatePath('special://home/addons/'+addonID+'/fanart.jpg')
iconsp  = xbmc.translatePath('special://home/addons/'+addonID+'/resources/imgs/iconsp.png')

socket.setdefaulttimeout(30)

addonUserDataFolder = xbmc.translatePath("special://profile/addon_data/"+addonID)

blacklist = addon.getSetting("blacklist").split(',')

infoEnabled  = addon.getSetting("showInfo") == "true"
infoType     = addon.getSetting("infoType")
infoDelay    = int(addon.getSetting("infoDelay"))
infoDuration = int(addon.getSetting("infoDuration"))

itSubCats = addon.getSetting("itSubCats") == "true"

forceVisu = addon.getSetting("forceVisu") == "true"
gensVisu  = str(addon.getSetting("gensVisu"))
plstVisu  = str(addon.getSetting("plstVisu"))

ytAddonURL = addon.getSetting("youtubeAddon")
ytAddonURL = ["plugin://plugin.video.youtube/play/?video_id=", "plugin://plugin.video.bromix.youtube/play/?video_id="][int(ytAddonURL)]

userAgent = "Mozilla/5.0 (Windows NT 6.1; rv:30.0) Gecko/20100101 Firefox/30.0"
opener = urllib2.build_opener()
opener.addheaders = [('User-Agent', userAgent)]

api_key = "AIzaSyCIM4EzNqi1in22f4Z3Ru3iYvLaY8tc3bo"

if not os.path.isdir(addonUserDataFolder) : os.mkdir(addonUserDataFolder)

baseIT = "https://itunes.apple.com/br/genre/music/id34"

def menu(url):
		conteudo = opener.open(url).read()
		conteudo = conteudo[conteudo.find('id="genre-nav"'):]
		conteudo = conteudo[:conteudo.find('</div>')]
		generos  = re.compile('<li><a href="https://itunes.apple.com/.+?/genre/.+?/id(.+?)"(.+?)title=".+?">(.+?)<', re.DOTALL).findall(conteudo)

		titIT = "Todos os Gêneros"

		if itSubCats : titIT = '[B]' + titIT + '[/B]'

		addAutoPlayDir(titIT, "0", "getvideos", "", "", "browse")

		for gen, tipo, tit in generos:
				tit = doLimpa(tit)
				
				if 'class="top-level-genre"' in tipo:
						if itSubCats : tit = '[B]' + tit + '[/B]'
						
						addAutoPlayDir(tit, gen, "getvideos", "", "", "browse")
						
				elif itSubCats:
						tit = '   ' + tit
						addAutoPlayDir(tit, gen, "getvideos", "", "", "browse")
		
		if forceVisu : setViewGens()
						
def getVideos(type, genreID, limit):
		if type == "play":
				musicVideos = []
				playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
				playlist.clear()
				
		url = "https://itunes.apple.com/br/rss/topsongs/limit=200"

		if genreID != "0" : url += "/genre="+genreID

		url += "/explicit=true/json"

		conteudo = opener.open(url).read()
		conteudo = json.loads(conteudo)
		items    = conteudo['feed']['entry']
		pos      = 1

		for item in items:
				artista = item['im:artist']['label'].encode('utf-8')
				vTit    = item['im:name']['label'].encode('utf-8')
				
				if " (" in vTit : vTit = vTit[:vTit.rfind(" (")]
				
				titulo = doLimpa(artista + " - " + vTit)
				
				try    : img = item['im:image'][2]['label'].replace("170x170-75.jpg","400x400-75.jpg")
				except : img = ""
				
				filtro = False
				
				for entry2 in blacklist:
						if entry2.strip().lower() and entry2.strip().lower() in title.lower(): filtro = True
						
				if filtro : continue
				
				if type == "browse":
						addLink(titulo, titulo.replace(" - ", " "), "playvideo", img)
				else:
						url = "plugin://"+addonID+"/?url="+urllib.quote_plus(titulo.replace(" - ", " "))+"&mode=playvideo"
						
						musicVideos.append([titulo, url, img])
						
						if limit and int(limit)==pos : break
						
						pos+=1
						
		if type=="browse":
				if forceVisu : setViewPlst()
				
		else:
				random.shuffle(musicVideos)
				
				for mvTit, mvUrl, mvImg in musicVideos:
						listitem = xbmcgui.ListItem(mvTit, thumbnailImage=mvImg)
						playlist.add(mvUrl, listitem)
						
				xbmc.Player().play(playlist)

def playVideo(title):
    try:
				ytID = getYTID(title)
				
				url = ytAddonURL + ytID
				
				listitem = xbmcgui.ListItem(path=url)
				
				xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
				
				if infoEnabled : showInfo()
    except:
        pass

def getYTID(title):
		titYT  = urllib.quote_plus(title.lower())
		urlYT  = "https://www.googleapis.com/youtube/v3/search?part=snippet&max-results=1&order=relevance&q=%s&key=%s"% (titYT, api_key)
		contYT = opener.open(urlYT).read()
		ytID   = re.findall('"videoId": "(.*?)"',contYT,re.S)[0]

		return ytID

def queueVideo(url, name):
		playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
		listitem = xbmcgui.ListItem(name)
		playlist.add(url, listitem)        

def showInfo():
    count = 0
		
    while not xbmc.Player().isPlaying():
        xbmc.sleep(200)
				
        if count == 50 : break
				
        count += 1
				
    xbmc.sleep(infoDelay*1000)
		
    if infoType == "0":
        xbmc.executebuiltin('XBMC.ActivateWindow(12901)')
        xbmc.sleep(infoDuration*1000)
        xbmc.executebuiltin('XBMC.ActivateWindow(12005)')
				
    elif infoType == "1":
        siTit = 'Tocando Agora:'
        siVid = xbmc.getInfoLabel('VideoPlayer.Title').replace(","," ")
        siImg = xbmc.getInfoImage('VideoPlayer.Cover')
				
        xbmc.executebuiltin('XBMC.Notification(%s, %s, %s, %s)' % (siTit, siVid, infoDuration*1000, siImg))

def doLimpa(title):
    title = title.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&").replace("&#39;", "'").replace("&#039;", "'").replace("&quot;", "\"").replace("&szlig;", "ß").replace("&ndash;", "-")
    title = title.replace("&Auml;", "Ä").replace("&Uuml;", "Ü").replace("&Ouml;", "Ö").replace("&auml;", "ä").replace("&uuml;", "ü").replace("&ouml;", "ö")
    title = title.strip()
    return title
		
def setViewGens() :
		opcao = addon.getSetting('gensVisu')
		
		if   opcao == '0': xbmc.executebuiltin("Container.SetViewMode(50)")
		elif opcao == '1': xbmc.executebuiltin("Container.SetViewMode(51)")
		elif opcao == '2': xbmc.executebuiltin("Container.SetViewMode(500)")
		
def setViewPlst() :
		opcao = addon.getSetting('plstVisu')

		if   opcao == '0': xbmc.executebuiltin("Container.SetViewMode(50)")
		elif opcao == '1': xbmc.executebuiltin("Container.SetViewMode(51)")
		elif opcao == '2': xbmc.executebuiltin("Container.SetViewMode(500)")
		elif opcao == '3': xbmc.executebuiltin("Container.SetViewMode(501)")
		elif opcao == '4': xbmc.executebuiltin("Container.SetViewMode(508)")
		elif opcao == '5': xbmc.executebuiltin("Container.SetViewMode(504)")
		elif opcao == '6': xbmc.executebuiltin("Container.SetViewMode(503)")
		elif opcao == '7': xbmc.executebuiltin("Container.SetViewMode(515)")
		
def addLink(name, url, mode, iconimage):
		u   = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
		ok  = True
		liz = xbmcgui.ListItem(name, iconImage=iconsp, thumbnailImage=iconimage)

		liz.setInfo(type="Video", infoLabels={"Title": name})
		liz.setProperty('fanart_image', fanart)
		liz.setProperty('IsPlayable', 'true')

		ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz)

		return ok

def addDir(name, url, mode, iconimage="", description="", type="", limit=""):
		u   = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&type="+str(type)+"&limit="+str(limit)
		ok  = True
		liz = xbmcgui.ListItem(name, iconImage=iconsp, thumbnailImage=iconimage)
		
		liz.setProperty('fanart_image', fanart)
		liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": description})
		
		ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
		
		return ok

def addAutoPlayDir(name, url, mode, iconimage="", description="", type="", limit=""):
		u   = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&type="+str(type)+"&limit="+str(limit)
		ok  = True
		liz = xbmcgui.ListItem(name, iconImage=iconsp, thumbnailImage=iconimage)
		
		liz.setProperty('fanart_image', fanart)
		liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": description})
		
		entries = []
		entries.append(("Autoplay Todos", 'RunPlugin(plugin://'+addonID+'/?mode='+str(mode)+'&url='+urllib.quote_plus(url)+'&type=play&limit=)',))
		entries.append(("Autoplay 10"   , 'RunPlugin(plugin://'+addonID+'/?mode='+str(mode)+'&url='+urllib.quote_plus(url)+'&type=play&limit=10)',))
		entries.append(("Autoplay 20"   , 'RunPlugin(plugin://'+addonID+'/?mode='+str(mode)+'&url='+urllib.quote_plus(url)+'&type=play&limit=20)',))
		entries.append(("Autoplay 30"   , 'RunPlugin(plugin://'+addonID+'/?mode='+str(mode)+'&url='+urllib.quote_plus(url)+'&type=play&limit=30)',))
		entries.append(("Autoplay 40"   , 'RunPlugin(plugin://'+addonID+'/?mode='+str(mode)+'&url='+urllib.quote_plus(url)+'&type=play&limit=40)',))
		entries.append(("Autoplay 50"   , 'RunPlugin(plugin://'+addonID+'/?mode='+str(mode)+'&url='+urllib.quote_plus(url)+'&type=play&limit=50)',))
		entries.append(("Autoplay 100"  , 'RunPlugin(plugin://'+addonID+'/?mode='+str(mode)+'&url='+urllib.quote_plus(url)+'&type=play&limit=100)',))
		entries.append(("Autoplay 150"  , 'RunPlugin(plugin://'+addonID+'/?mode='+str(mode)+'&url='+urllib.quote_plus(url)+'&type=play&limit=150)',))
		
		liz.addContextMenuItems(entries)
		ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
		return ok
		
def getParams(parameters):
		paramDict = {}

		if parameters : 
				paramPairs = parameters[1:].split("&")
				
				for paramsPair in paramPairs:
						paramSplits = paramsPair.split('=')
						
						if (len(paramSplits)) == 2 : paramDict[paramSplits[0]] = paramSplits[1]
						
		return paramDict

params    = getParams(sys.argv[2])
mode      = urllib.unquote_plus(params.get('mode', ''))
url       = urllib.unquote_plus(params.get('url', ''))
name      = urllib.unquote_plus(params.get('name', ''))
iconimage = urllib.unquote_plus(params.get('iconimage', ''))
type      = urllib.unquote_plus(params.get('type', ''))
limit     = urllib.unquote_plus(params.get('limit', ''))

if   mode == ''           : menu(url=baseIT)
elif mode == 'getvideos'  : getVideos(type, url, limit)
elif mode == 'playvideo'  : playVideo(url)
elif mode == 'queueVideo' : queueVideo(url, name)
    
xbmcplugin.endOfDirectory(int(sys.argv[1]))

# -*- coding: utf-8 -*-
#
# 21/08/2015 - By AddonBrasil
###############################################################################

import xbmc,xbmcaddon,xbmcgui,xbmcplugin
import urllib,urllib2,os,re,sys,datetime,time
import plugintools

###############################################################################

addon_id    = 'plugin.video.sbtonline'
selfAddon   = xbmcaddon.Addon(id=addon_id)
datapath    = xbmc.translatePath(selfAddon.getAddonInfo('profile'))
addonfolder = selfAddon.getAddonInfo('path')

icon        = addonfolder + '/icon.png'
fanart      = addonfolder + '/fanart.jpg'
artfolder   = addonfolder + '/resources/art/'

base = 'plugin://plugin.video.youtube/channel/'

###############################################################################

def menuPrincipal():
		plugintools.add_item(title="A Praça é Nossa",url=base+"UCMUcTceXYCuCyGTNMNvc1qQ/",thumbnail=artfolder+'apraca.jpg',fanart=fanart,folder=True)
		plugintools.add_item(title="Bake off Brasil",url=base+"UCw2WDC9gc0jzoHsoRAzR9Yw/",thumbnail=artfolder+'bake.jpg',fanart=fanart,folder=True)
		plugintools.add_item(title="Carrossel",url=base+"UC62chqw1TwkDl93iS8RzT1g/",thumbnail=artfolder+'carrossel.jpg',fanart=fanart,	folder=True)
		plugintools.add_item(title="Chiquititas",url=base+"UCRc1QYRg0L0q53wMAvUMxyg/",thumbnail=artfolder+'chiquititas.jpg',fanart=fanart,folder=True)
		plugintools.add_item(title="Cozinha Sob Pressão",url=base+"UC-S82QSyHb-e3FddEO6Tq6w/",thumbnail=artfolder+'cozinha.jpg',fanart=fanart,folder=True)
		plugintools.add_item(title="Cúmplices de um Resgate",url=base+"UCvzAkazTwM1mdF84PaLud5Q/",thumbnail=artfolder+'cumplices.jpg',fanart=fanart,folder=True)
		plugintools.add_item(title="Domingo Legal",url=base+"UCZjZZc4lE_pPEKvAjKQhQbg/",thumbnail=artfolder+'domingo.jpg',fanart=fanart,folder=True)
		plugintools.add_item(title="Esquadrão da Moda",url=base+"UCuXAGHXIXpplEwAAKzlks_w/",thumbnail=artfolder+'esquadrao.jpg',fanart=fanart,folder=True)
		plugintools.add_item(title="Esse Artista Sou Eu",url=base+"UCwo6zImDS9CgZDn3d-6liXA/",thumbnail=artfolder+'esse.jpg',fanart=fanart,folder=True)
		plugintools.add_item(title="Jornalismo SBT",url=base+"UC376n347Ob5Lwzq2WGzF1AA/",thumbnail=artfolder+'jornalismo.jpg',fanart=fanart,folder=True)
		plugintools.add_item(title="Maquina da Fama",url=base+"UC3cvGhRDHbQHtE1a9CH5ZYg/",thumbnail=artfolder+'maquina.jpg',fanart=fanart,folder=True)
		plugintools.add_item(title="OK Pessoal",url=base+"UCd8gSv7nDBd2xuN5nLnIeBQ/",thumbnail=artfolder+'okpessoal.jpg',fanart=fanart,folder=True)
		plugintools.add_item(title="Programa Eliana",url=base+"UCgIGfejXEuZZj88ibShbDVg/",thumbnail=artfolder+'eliana.jpg',fanart=fanart,folder=True)
		plugintools.add_item(title="Programa Silvio Santos",url=base+"UC-5npwFvOH9Mp_a15T0VT9g/",thumbnail=artfolder+'pss.jpg',fanart=fanart,folder=True)
		plugintools.add_item(title="SBT Games",url=base+"UCA3ruDoERVJuT6JMGZ9HNmw/",thumbnail=artfolder+'sbtgames.jpg',fanart=fanart,folder=True)
		plugintools.add_item(title="The Noite",url=base+"UCEWOoncsrmirqnFqxer9lmA/",thumbnail=artfolder+'thenoite.jpg',fanart=fanart,folder=True)
			
		xbmcplugin.setContent(int(sys.argv[1]), 'movies')
		xbmc.executebuiltin('Container.SetViewMode(500)')
		
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
url       = None
name      = None
iconimage = None
mode      = None

try    : url = urllib.unquote_plus(params["url"])
except : pass
try    : name = urllib.unquote_plus(params["name"])
except : pass
try    : mode = int(params["mode"])
except : pass
try    : iconimage = urllib.unquote_plus(params["iconimage"])
except : pass

###############################################################################

print "Mode : " + str(mode)
print "Icon : " + str(iconimage)
print "URL  : " + str(url)
print "Name : " + str(name)

if   mode == None : menuPrincipal() 

xbmcplugin.endOfDirectory(int(sys.argv[1]))

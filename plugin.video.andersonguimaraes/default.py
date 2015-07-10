# -*- coding: utf-8 -*-
#------------------------------------------------------------
# http://www.youtube.com/user/andersonrel
#------------------------------------------------------------
# Licença: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Baseado no código do addon youtube
#------------------------------------------------------------

import os
import sys
import plugintools
import xbmc,xbmcaddon
from addon.common.addon import Addon

addonID = 'plugin.video.andersonguimaraes'
addon = Addon(addonID, sys.argv)
local = xbmcaddon.Addon(id=addonID)
icon = local.getAddonInfo('icon')

addonfolder = local.getAddonInfo('path')
resfolder = addonfolder + '\\resources'


YOUTUBE_CHANNEL_ID = "andersonrel"

# Ponto de Entrada
def run():
	plugintools.log("andersonrel.run")

	entryurl=str(resfolder)+"\\entrada.mp4"
	plugintools.direct_play(str(entryurl))

	# Pega Parâmetros
	params = plugintools.get_params()

	if params.get("action") is None:
		main_list(params)
	else:
		action = params.get("action")
		exec action+"(params)"

	plugintools.close_item_list()

# Menu Principal
def main_list(params):
    plugintools.log("andersonrel.main_list "+repr(params))

    plugintools.add_item(
				title = "Canal do Anderson Guimarães",
        url = "plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID+"/",
        thumbnail = icon,
        folder = True )

run()
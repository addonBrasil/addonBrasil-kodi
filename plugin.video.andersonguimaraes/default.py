# -*- coding: utf-8 -*-
#------------------------------------------------------------
# http://www.youtube.com/user/andersonrel
#------------------------------------------------------------
# Licença: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Baseado no código do addon youtube
#------------------------------------------------------------

import os, sys, time, plugintools, xbmc, xbmcaddon

from addon.common.addon import Addon

addonID = 'plugin.video.andersonguimaraes'
addon   = Addon(addonID, sys.argv)
local   = xbmcaddon.Addon(id=addonID)
icon    = local.getAddonInfo('icon')

YOUTUBE_CHANNEL_ID = "andersonrel"

def run():
	params = plugintools.get_params()
	
	if params.get("action") is None: 
		main_list(params)
	else:
		action = params.get("action")
		exec action+"(params)"

	plugintools.close_item_list()

def main_list(params):
	plugintools.log("andersonrel.main_list "+repr(params))
	
	plugintools.log("andersonrel.run")
	
	plugintools.add_item(
		title = "Canal do Anderson Guimarães",
		url = "plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID+"/",
		thumbnail = icon,
		folder = True )

run()
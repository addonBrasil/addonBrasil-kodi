#------------------------------------------------------------
# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Licença: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Baseado no código do addon youtube
#------------------------------------------------------------

import os, sys, time, plugintools, xbmc, xbmcaddon

from addon.common.addon import Addon

addonID = 'plugin.video.osmelhoresdomundo'
addon   = Addon(addonID, sys.argv)
local   = xbmcaddon.Addon(id=addonID)
icon    = local.getAddonInfo('icon')

print icon

YOUTUBE_CHANNEL_ID = "ComediaMM"

def run():
	params = plugintools.get_params()
	
	if params.get("action") is None: 
		main_list(params)
	else:
		action = params.get("action")
		exec action+"(params)"

	plugintools.close_item_list()

def main_list(params):
	plugintools.log("osmelhoresdomundo "+repr(params))
	
	plugintools.log("osmelhoresdomundo.run")
	
	plugintools.add_item(
		title = "Os Melhores Do Mundo",
		url = "plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID+"/",
		thumbnail = 'https://yt3.ggpht.com/-w1yDMKm7dvU/AAAAAAAAAAI/AAAAAAAAAAA/5wIM9Mn7-Tc/s100-c-k-no-mo-rj-c0xffffff/photo.jpg',
		folder = True )

run()
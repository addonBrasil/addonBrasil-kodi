# -*- coding: utf-8 -*-
#------------------------------------------------------------
# http://www.youtube.com/user/SuperSimpleSongs
#------------------------------------------------------------
# Licença: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Baseado no código do addon youtube
#------------------------------------------------------------

import os
import sys
import time
import plugintools
import xbmc,xbmcaddon
from addon.common.addon import Addon

addonID = 'plugin.video.sss'
addon = Addon(addonID, sys.argv)
local = xbmcaddon.Addon(id=addonID)
icon = local.getAddonInfo('icon')

#addonfolder = local.getAddonInfo('path')

YOUTUBE_CHANNEL_ID = "SuperSimpleSongs"

def run():
	params = plugintools.get_params()
	
	if params.get("action") is None:
		main_list(params)
	else:
		action = params.get("action")
		exec action+"(params)"

	plugintools.close_item_list()

def main_list(params):
	plugintools.log("sss.main_list "+repr(params))
	plugintools.log("sss.run")
	
	plugintools.add_item(
		title = "Canal Super Simple Songs",
		url = "plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID+"/",
		thumbnail = icon,
		folder = True )
		
run()
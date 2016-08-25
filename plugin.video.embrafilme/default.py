# -*- coding: utf-8 -*-
#------------------------------------------------------------
# http://www.youtube.com/user/andersonrel
#------------------------------------------------------------
# Licença: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Baseado no código do addon youtube
#------------------------------------------------------------

import os, sys, time, plugintools, xbmc, xbmcaddon

from addon.common.addon import Addon

addonID = 'plugin.video.embrafilme'
addon   = Addon(addonID, sys.argv)
local   = xbmcaddon.Addon(id=addonID)
icon    = local.getAddonInfo('icon')

ID = "Embrafilme"

def run():
	params = plugintools.get_params()
	
	if params.get("action") is None: 
		main_list(params)
	else:
		action = params.get("action")
		exec action+"(params)"

	plugintools.close_item_list()

def main_list(params):
	plugintools.log("embrafilme.main_list "+repr(params))
	
	plugintools.log("embrafilme.run")
	
	plugintools.add_item(
		title = "Canal Embrafilme",
		url = "plugin://plugin.video.youtube/user/" + ID +"/",
		thumbnail = icon,
		folder = True )

run()
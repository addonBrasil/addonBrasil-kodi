# -*- coding: utf-8 -*-
#------------------------------------------------------------
# http://www.youtube.com/user/OMundo2osBrasileiros
#------------------------------------------------------------
# Licença: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Baseado no código do addon youtube
#------------------------------------------------------------

import xbmc, xbmcaddon, xbmcplugin, os, sys, plugintools

from addon.common.addon import Addon

addonID = 'plugin.video.docbrasil'
addon   = Addon(addonID, sys.argv)
local   = xbmcaddon.Addon(id=addonID)
icon    = local.getAddonInfo('icon')
base    = 'plugin://plugin.video.youtube/'

icon1 = 'https://yt3.ggpht.com/-AG3B5JcuJvY/AAAAAAAAAAI/AAAAAAAAAAA/0gwVUumgRFw/s176-c-k-no/photo.jpg'
icon2 = 'https://yt3.ggpht.com/-yVgJ1eTSMoE/AAAAAAAAAAI/AAAAAAAAAAA/TeiFq2epjR0/s176-c-k-no/photo.jpg'
icon3 = 'https://yt3.ggpht.com/-pYkB_ZP_RIg/AAAAAAAAAAI/AAAAAAAAAAA/vDny9JtvyUw/s176-c-k-no/photo.jpg'
icon4 = 'https://yt3.ggpht.com/-i05g9SymCKw/AAAAAAAAAAI/AAAAAAAAAAA/NyZkelG1IsI/s176-c-k-no/photo.jpg'
icon5 = 'https://yt3.ggpht.com/-Od5C_pWlowM/AAAAAAAAAAI/AAAAAAAAAAA/Bj02jHz6mho/s176-c-k-no/photo.jpg'
icon6 = 'https://yt3.ggpht.com/-6oiqLNdUoeE/AAAAAAAAAAI/AAAAAAAAAAA/SCdFFNnVyhk/s176-c-k-no/photo.jpg'
icon7 = 'https://yt3.ggpht.com/-Kwp5EzxFFAU/AAAAAAAAAAI/AAAAAAAAAAA/HeggNByF-oA/s176-c-k-no/photo.jpg'
icon8 = 'https://yt3.ggpht.com/-KkueCbnKFfc/AAAAAAAAAAI/AAAAAAAAAAA/tVe-nrgg0mc/s176-c-k-no/photo.jpg'
icon9 = 'https://yt3.ggpht.com/-0Si5qmcUhW4/AAAAAAAAAAI/AAAAAAAAAAA/NBsH0xbG-GU/s176-c-k-no/photo.jpg'
icon0 = 'https://yt3.ggpht.com/-tqsCbyWrsso/AAAAAAAAAAI/AAAAAAAAAAA/po-c8qsWGFw/s176-c-k-no/photo.jpg'

def run():
    plugintools.log("DocBrasil.run")
    
    params = plugintools.get_params()
    
    if params.get("action") is None:
        main_list(params)
    else:
        action = params.get("action")
        exec action+"(params)"
    
    plugintools.close_item_list()

def main_list(params):
		plugintools.log("DocBrasil ===> " + repr(params))

		plugintools.add_item(title = "BBC Documentários HD"          , url = base + "user/BBCnosferahcorp/"            , thumbnail = icon1, folder = True)
		plugintools.add_item(title = "Documentários Completos HD"    , url = base + "channel/UCGPHwBqiE0aCWw7ORVYYrKg/", thumbnail = icon2, folder = True)
		plugintools.add_item(title = "Documentários Premium"         , url = base + "channel/UC6U6wWtsiG78RAWeXwAt4FA/", thumbnail = icon3, folder = True)
		plugintools.add_item(title = "Documentários Premium HD"      , url = base + "channel/UCwVvTMndCn2srfxIIxeovJw/", thumbnail = icon4, folder = True)
		plugintools.add_item(title = "Documentários Ptfelicitas"     , url = base + "user/ptfelicitas/"                , thumbnail = icon5, folder = True)
		plugintools.add_item(title = "Documentários Varios"          , url = base + "channel/UCWNliaGcc5dCg4slJgDkPgw/", thumbnail = icon6, folder = True)
		plugintools.add_item(title = "Full Documentário"             , url = base + "channel/UCUYRspxQAioXtIVXcnPP6Pg/", thumbnail = icon7, folder = True)
		plugintools.add_item(title = "Super Documentários"           , url = base + "channel/UCCI5enlYrd0H96PKF16ChTQ/", thumbnail = icon8, folder = True)
		plugintools.add_item(title = "Universo Dos Documentários"    , url = base + "channel/UCnnXcMPdZbB0lvcvBQ5KE5g/", thumbnail = icon9, folder = True)
		plugintools.add_item(title = "Visão do Mundo - Documentários", url = base + "channel/UCcPud6tzYnYAdoFWNDisu1g/", thumbnail = icon0, folder = True)

		
		
		xbmcplugin.setContent(int(sys.argv[1]), 'movies')
		xbmc.executebuiltin('Container.SetViewMode(500)')
		
run()
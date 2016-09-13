# -*- coding: utf-8 -*-
#------------------------------------------------------------
# TV Cultura Digital
#------------------------------------------------------------
# Licença: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Baseado no código do addon youtube
#------------------------------------------------------------

import xbmc, xbmcaddon, xbmcplugin, os, sys, plugintools
from addon.common.addon import Addon

addonID = 'plugin.video.tvculturadigital'
addon   = Addon(addonID, sys.argv)
local   = xbmcaddon.Addon(id=addonID)
icon    = local.getAddonInfo('icon')
fan     = local.getAddonInfo('fanart')
baseU   = 'plugin://plugin.video.youtube/user/'
baseC   = 'plugin://plugin.video.youtube/channel/'
baseI   = 'special://home/addons/'+addonID+'/resources/imgs/'

def run():
	plugintools.log("tvculturadigital.run")
	
	params = plugintools.get_params()
	
	if params.get("action") is None: main_list(params)
	else:
			action = params.get("action")
			exec action+"(params)"
			
	plugintools.close_item_list()

def main_list(params):
	plugintools.log("tvculturadigital ===> " + repr(params))

	plugintools.add_item(title= "TV Cultura Digital"   , url=baseU+"cultura/"                 , thumbnail=baseI+'tvc.png', fanart = fan, folder = True)
	plugintools.add_item(title= "Cartão Verde"         , url=baseC+"UC01ScqANYPir48jBi2zsuyw/", thumbnail=baseI+'cv.png' , fanart = fan, folder = True)
	plugintools.add_item(title= "Castelo Ra-Ti-Bum"    , url=baseU+"videocasteloratimbum/"    , thumbnail=baseI+'rtb.png', fanart = fan, folder = True)
	plugintools.add_item(title= "Cocoricó"             , url=baseU+"tvcocorico/"              , thumbnail=baseI+'crc.png', fanart = fan, folder = True)
	plugintools.add_item(title= "Cultura Livre"        , url=baseU+"culturalivre/"            , thumbnail=baseI+'cl.png' , fanart = fan, folder = True)
	plugintools.add_item(title= "Jornalismo TV Cultura", url=baseU+"jornaldacultura/"         , thumbnail=baseI+'jtc.png', fanart = fan, folder = True)	
	plugintools.add_item(title= "Manos e Minas"        , url=baseU+"ManosEMinasTVCultura/"    , thumbnail=baseI+'mm.png' , fanart = fan, folder = True)
	plugintools.add_item(title= "Matéria de Capa"      , url=baseU+"MateriaDeCapa/"           , thumbnail=baseI+'mc.png' , fanart = fan, folder = True)
	plugintools.add_item(title= "Ordem Do Dia"         , url=baseC+"UCZJ-3LBr4h-yKtWsjeQTq_A/", thumbnail=baseI+'od.png' , fanart = fan, folder = True)
	plugintools.add_item(title= "Persona Em Foco"      , url=baseC+"UC9KKZwr5Yx5UU3KRt9dlOGA/", thumbnail=baseI+'pef.png', fanart = fan, folder = True)
	plugintools.add_item(title= "Programa Ensaio"      , url=baseU+"EnsaioTVCultura/"         , thumbnail=baseI+'pe.png' , fanart = fan, folder = True)
	plugintools.add_item(title= "Programa Prelúdio"    , url=baseU+"ProgramaPreludio/"        , thumbnail=baseI+'pp.png' , fanart = fan, folder = True)
	plugintools.add_item(title= "Provocações"          , url=baseC+"UCKdVW7Np-9l3CM5daYcGEAw/", thumbnail=baseI+'pro.png', fanart = fan, folder = True)
	plugintools.add_item(title= "Quintal da Cultutra"  , url=baseU+"quintaldacultura/"        , thumbnail=baseI+'qc.png' , fanart = fan, folder = True)
	plugintools.add_item(title= "Repórter Eco"         , url=baseC+"UCxXiasLNEA7gO3k22qRsaUA/", thumbnail=baseI+'re.png' , fanart = fan, folder = True)
	plugintools.add_item(title= "Roda Viva"            , url=baseU+"rodaviva/"                , thumbnail=baseI+'rv.png' , fanart = fan, folder = True)
	plugintools.add_item(title= "Sr. Brasil"           , url=baseU+"SrBrasilTVCultura/"       , thumbnail=baseI+'srb.png', fanart = fan, folder = True)
	plugintools.add_item(title= "TV Univesp"           , url=baseU+"univesptv/"               , thumbnail=baseI+'tvu.png', fanart = fan, folder = True)
	plugintools.add_item(title= "Viola, Minha Viola"   , url=baseU+"ViolaTVCultura/"          , thumbnail=baseI+'vmv.png', fanart = fan, folder = True)

run()

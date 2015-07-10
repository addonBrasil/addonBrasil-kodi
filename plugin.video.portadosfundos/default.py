# -*- coding: utf-8 -*-
#------------------------------------------------------------
# http://www.youtube.com/user/GoProCamera
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Based on code from youtube addon
#------------------------------------------------------------

import os
import sys
import plugintools

YOUTUBE_CHANNEL_ID = "UCEWHPFNilsT0IfQfutVzsag"

# Entry point
def run():
    plugintools.log("UCEWHPFNilsT0IfQfutVzsag.run")
    
    # Get params
    params = plugintools.get_params()
    
    if params.get("action") is None:
        main_list(params)
    else:
        action = params.get("action")
        exec action+"(params)"
    
    plugintools.close_item_list()

# Main menu
def main_list(params):
    plugintools.log("UCEWHPFNilsT0IfQfutVzsag.main_list "+repr(params))

    # On first page, pagination parameters are fixed
    if params.get("url") is None:
        params["url"] = "http://gdata.youtube.com/feeds/api/users/"+YOUTUBE_CHANNEL_ID+"/uploads?start-index=1&max-results=10"

    # Fetch video list from YouTube feed
    data = plugintools.read( params.get("url") )
    
    # Extract items from feed
    pattern = ""
    matches = plugintools.find_multiple_matches(data,"<entry>(.*?)</entry>")
    
    for entry in matches:
        
        # Not the better way to parse XML, but clean and easy
        title = plugintools.find_single_match(entry,"<titl[^>]+>([^<]+)</title>")
        plot = plugintools.find_single_match(entry,"<media\:descriptio[^>]+>([^<]+)</media\:description>")
        thumbnail = plugintools.find_single_match(entry,"<media\:thumbnail url='([^']+)'")
        video_id = plugintools.find_single_match(entry,"http\://www.youtube.com/watch\?v\=([^\&]+)\&").replace("&amp;","&")
        url = "plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid="+video_id

        # Appends a new item to the xbmc item list
        plugintools.add_item( action="play" , title=title , plot=plot , url=url ,thumbnail=thumbnail , folder=True )
    
    # Calculates next page URL from actual URL
    start_index = int( plugintools.find_single_match( params.get("url") ,"start-index=(\d+)") )
    max_results = int( plugintools.find_single_match( params.get("url") ,"max-results=(\d+)") )
    next_page_url = "http://gdata.youtube.com/feeds/api/users/"+YOUTUBE_CHANNEL_ID+"/uploads?start-index=%d&max-results=%d" % ( start_index+max_results , max_results)

    plugintools.add_item( action="main_list" , title=">> Próxima página" , url=next_page_url , folder=True )

def play(params):
    plugintools.play_resolved_url( params.get("url") )

run()
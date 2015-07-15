# coding = utf-8
#!/usr/bin/python

import pylast,sys,os
import time,datetime

get_state = """osascript -e 'tell application "iTunes" to player state as string'"""
get_artist = """osascript -e 'tell application "iTunes" to artist of current track as string'"""
get_title = """osascript -e 'tell application "iTunes" to name of current track as string'"""
get_postion="""osascript -e 'tell app "itunes" to player position'"""
get_duration="""osascript -e 'tell app "itunes" to duration of current track'"""

if __name__ == "__main__":
    API_KEY = sys.argv[1]
    API_SECRET = sys.argv[2]
    username = sys.argv[3]
    password_hash = pylast.md5(sys.argv[4])
    network = pylast.LastFMNetwork(api_key = API_KEY, api_secret = API_SECRET, username = username, password_hash = password_hash)
    while True:
        if os.popen(get_state).read().strip('\n') == "playing":
            artist = os.popen(get_artist).read().strip('\n')
            title = os.popen(get_title).read().strip('\n')
            unixTimestamp = int(time.mktime(datetime.datetime.now().timetuple()))
            network.scrobble(artist=artist,title=title,timestamp = unixTimestamp)
            current_position = os.popen(get_postion).read().strip('\n')
            current_duration = os.popen(get_duration).read().strip('\n')
            sleep_time = float(current_duration) - float(current_position) + 5
            print sleep_time,unixTimestamp, artist, title
            print "up"
            time.sleep(sleep_time);
        else:
            print "nothing to submit"
            time.sleep(60)

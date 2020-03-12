import os
import sys
import time
from gooey import Gooey
from gooey import GooeyParser
import pafy
from pytube import Playlist

running = True
pListUrl = []
pathToSave = None

@Gooey(optional_cols=2,
       program_name="Youtube Downloader",
       dump_build_config=True,
        show_success_modal=False)
def main():
    settings_msg = 'YouTube URL Parsing Tool. Downloads single videos, songs, as well as playlists '
    parser = GooeyParser(description=settings_msg)

    parser.add_argument('--verbose', help='be verbose', dest='verbose',action='store_true', default=False)

    subs = parser.add_subparsers(help='singlevid', dest='command')

    singleVideo = subs.add_parser('single-video', help='Downloads a single video from a YouTube url')
    singleVideo.add_argument("--YouTube_Video_Url", help="Enter your YouTube Link to Download")
    singleVideo.add_argument('--Save_Location', help="Select where to download the video to", widget="DirChooser")

    playlistVideo = subs.add_parser('video-playlist', help='Downloads a playlist of videos from a YouTube url')
    playlistVideo.add_argument("--YouTube_Playlist_Url", help="Enter your YouTube Playlist URL to Download")
    playlistVideo.add_argument('--Playlist_Save_Location', help="Select where to download the playlist to", widget="DirChooser")

    singleAudio = subs.add_parser('single-audio', help='Downloads a single song from a YouTube url')
    singleAudio.add_argument("--YouTube_Audio_Url", help="Enter your YouTube Link to Download")
    singleAudio.add_argument('--Save_Location_Audio', help="Select where to download the video to", widget="DirChooser")

    playlistAudio = subs.add_parser('audio-playlist', help='Downloads a playlist of songs from a YouTube url')
    playlistAudio.add_argument("--YouTube_Playlist_Url", help="Enter your YouTube Playlist URL to Download")
    playlistAudio.add_argument('--Playlist_Save_Location', help="Select where to download the playlist to", widget="DirChooser")

    args = parser.parse_args()

    command = args.command

    print(args)

    if "single-video" in command:
        tUrl =args.YouTube_Video_Url
        pathToSave = args.Save_Location
        getOneVid(tUrl,pathToSave)

    elif "video-playlist" in command:
        setPlayList(args)
        getAllVids(args)

    elif "single-audio" in command:

        getOneSong(args)

    elif "audio-playlist" in command:
        setPlayList(args)
        getAllSongs(args)

def getOneVid(urlToDl,path):
    video = pafy.new(urlToDl)
    print("Getting best video")
    vDL = video.getbest(preftype="mp4")
    print("Got best video")
    print("Now downloading: "+vDL.title)
    createDir(vDL.title)
    vDL.download(filepath=path,quiet=False)
    print("download complete")
    print("now sleeping")
    time.sleep(2)

def getOneSong(urlToDl,path):
    video = pafy.new(urlToDl)
    print("Getting best video")
    sDL = video.getbestaudio()
    print("Got best video")
    print("Now downloading: "+sDL.title)
    createDir(sDL.title)
    sDL.download(filepath=path,quiet=False)
    print("download complete")
    print("now sleeping")
    time.sleep(2)

def setPlayList(url):

    try:
        pList = Playlist(url)

        if not pList:
            print("Unable to parse playlist url")

        else:
            pList.populate_video_urls()

            #iteraets throug urls populated and appends them to list

            for v in pList.video_urls:
                tVideo = pafy.new(v)

                pListUrl.append(tVideo)

            print("Playlist parsed sucessfully. Ready for downloading")


    except:
        print("Error parsing URL object")
        sys.exit(status=Exception)



def getAllVids(pListUrl):
    for v in pListUrl:
        getOneVid(v,pathToSave)


def getAllSongs(pListUrl):
    for v in pListUrl:
        getOneSong(v,pathToSave)


def createDir(dir):

    if os._exists(dir):
        print("Destination directory already exists")

    else:
        print("Creating output folder")
        try:
            os.mkdir(dir)
        except:
            print("Unable to make output folder. will save file in current directory")
            dir = os.getcwd()

if __name__ == '__main__':
    main()
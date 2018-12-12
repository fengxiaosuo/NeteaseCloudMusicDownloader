#!/usr/bin/env python3

"""
# Music detail
```python
http://music.163.com/api/song/detail/?id={Song id}&ids=[{Song id}]
```

# Test
```python
headers = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}
url_base = "http://music.163.com/api/song/detail/?id={}&ids=[{}]"
song_id = "441116287"
url = url_base.format(song_id, song_id)
# Without headers will return with resp.text='{"code":-460,"msg":"Cheating"}'
resp = requests.get(url, headers=headers)
rr = json.loads(resp.text)

print(rr['songs'][0]['name'])
print(rr['songs'][0]['artists'][0]['name'])
print(rr['songs'][0]['album']['name'])
print(rr['songs'][0]['album']['artists'][0]['name'])

source_path = '/home/leondgarse/.cache/netease-cloud-music/CachedSongs'
file_contents = os.listdir(source_path)
song_id = file_contents[0].split('-')[0]

import eyed3
tt = eyed3.load(source_path + '/' + file_contents[0])

tt.tag.title = rr['songs'][0]['name']
tt.tag.artist = rr['songs'][0]['artists'][0]['name']
tt.tag.album = rr['songs'][0]['album']['name']
tt.tag.album_artist = rr['songs'][0]['album']['artists'][0]['name']
tt.tag.save()
tt.tag.save(encoding="utf8")
```
"""

import requests
import json
import os
import sys
import argparse
import eyed3
import shutil
from datetime import datetime


def detect_netease_music_name(song_id):
    headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0"}
    url_base = "http://music.163.com/api/song/detail/?id={}&ids=[{}]"

    url_target = url_base.format(song_id, song_id)
    resp = requests.get(url_target, headers=headers)
    rr = json.loads(resp.text)

    song_info = {}
    song_info["title"] = rr["songs"][0]["name"].replace("\xa0", " ")
    song_info["artist"] = rr["songs"][0]["artists"][0]["name"]
    song_info["album"] = rr["songs"][0]["album"]["name"]
    song_info["album_artist"] = rr["songs"][0]["album"]["artists"][0]["name"]
    song_info["track_num"] = (rr["songs"][0]["no"], None)
    song_info["year"] = str(datetime.fromtimestamp(int(rr["songs"][0]["album"]["publishTime"]) / 1000).year)

    return song_info, rr


def detect_netease_music_name_list(song_list):
    for song_id in song_list:
        ss, rr = detect_netease_music_name(song_id)
        ss.update({"song_id": song_id})
        yield ss


def generate_target_file_name(dist_path, title, artist, song_format="mp3"):
    aa = artist.replace("/", " ").replace(":", " ").replace("?", " ").strip()
    tt = title.replace("/", " ").replace(":", " ").replace("?", " ").strip()
    dist_name = os.path.join(dist_path, "%s - %s" % (aa, tt)) + "." + song_format

    return dist_name


def netease_cache_rename_single(song_id, file_path, dist_path, KEEP_SOURCE=True, song_format="mp3", SAVE_COVER_IAMGE=True):
    if not os.path.exists(dist_path):
        os.mkdir(dist_path)

    song_info, rr = detect_netease_music_name(song_id)
    tt = eyed3.load(file_path)
    tt.tag.title = song_info["title"]
    tt.tag.artist = song_info["artist"]
    tt.tag.album = song_info["album"]
    tt.tag.album_artist = song_info["album_artist"]
    tt.tag.track_num = song_info["track_num"]
    tt.tag.recording_date = eyed3.core.Date.parse(song_info["year"])
    print(
        "song_id = %s, tt.tag {title = %s, artist = %s, album = %s, album_artist = %s, track_num = %s, year = %s}"
        % (song_id, tt.tag.title, tt.tag.artist, tt.tag.album, tt.tag.album_artist, tt.tag.track_num, song_info["year"])
    )

    if SAVE_COVER_IAMGE:
        pic_url = rr["songs"][0]["album"]["blurPicUrl"]
        resp = requests.get(pic_url)
        tt.tag.images.set(3, resp.content, "image/jpeg", "album cover")
    tt.tag.save(encoding="utf8")

    dist_name = generate_target_file_name(dist_path, tt.tag.title, tt.tag.artist, song_format)

    if KEEP_SOURCE == True:
        shutil.copyfile(file_path, dist_name)
    else:
        os.rename(file_path, dist_name)

    return dist_name


def netease_cache_rename(source_path, dist_path, KEEP_SOURCE=True):
    for file_name in os.listdir(source_path):
        if not file_name.endswith(".mp3"):
            continue
        if not len(file_name.split("-")) == 3:
            print(">>>> File %s not in format <song id>-<bite rate>-<random number>.mp3" % (file_name))
            continue

        song_id = file_name.split("-")[0]
        netease_cache_rename_single(song_id, os.path.join(source_path, file_name), dist_path, KEEP_SOURCE)


def parse_arguments(argv):
    HOME_DIR = os.getenv("HOME")
    default_source_path = os.path.join(HOME_DIR, ".cache/netease-cloud-music/CachedSongs")
    default_dist_path = "./output_music"

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=(
            "Rename netease-cloud-music Ubuntu client cached files\n"
            "From: source_path/<song id>-<bite rate>-<random number>.mp3\n"
            "To: dist_path/<artist name> - <song title>.mp3\n"
            "\n"
            "default source path: %s\n"
            "default dist path: %s" % (default_source_path, default_dist_path)
        ),
    )
    parser.add_argument("-d", "--dist_path", type=str, help="Music output path", default=default_dist_path)
    parser.add_argument("-s", "--source_path", type=str, help="Music source path", default=default_source_path)
    parser.add_argument(
        "-r", "--remove_source", action="store_true", help="Remove source files, default using cp instead of mv"
    )

    args = parser.parse_args(argv)
    args.keep_source = not args.remove_source
    return args


if __name__ == "__main__":
    args = parse_arguments(sys.argv[1:])
    print("source = %s, dist = %s" % (args.source_path, args.dist_path))
    netease_cache_rename(args.source_path, args.dist_path, args.keep_source)

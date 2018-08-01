#!/usr/bin/env python3

"""
## Download
http://music.taihe.com/data/music/fmlink?songIds={song id}
http://music.baidu.com/data/music/fmlink?songIds={song id}
http://music.163.com/song/media/outer/url?id={Song id}.mp3

## playlist
https://music.163.com/#/playlist?id={play list}
http://music.163.com/api/playlist/detail?id={play list}

## Netease dowload 320K
headers = {
    'Accept': '*/*',
    'Host': 'music.163.com',
    'User-Agent': 'curl/7.51.0',
    'Referer': 'http://music.163.com',
    'Cookie': 'appver=2.0.2'
}
song_download_url = 'http://music.163.com/weapi/song/enhance/player/url?csrf_token='
params = {'ids': [song_id], 'br': bit_rate}

import encrypt
data = encrypt.encrypted_request(params)
rr = requests.post(song_download_url, data=data, timeout=30, headers=headers)
rr.json()
"""

import os
import sys
import argparse
import json
import requests
import netease_rename
import encrypt

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0"
}


def netease_parse_playlist_2_list(playlist_id):
    url_playlist_base = "http://music.163.com/api/playlist/detail?id={}"
    url_playlist = url_playlist_base.format(playlist_id)

    resp = requests.get(url_playlist, headers=headers)
    rr = json.loads(resp.text)
    play_list = rr["result"]["tracks"]

    for song_item in play_list:
        yield song_item["id"]


def get_url_2_local_file(song_id, url, dist_path, WITH_RENAME=True, song_format="mp3"):
    song_info, _ = netease_rename.detect_netease_music_name(song_id)
    dist_name = netease_rename.generate_target_file_name(
        dist_path, song_info["title"], song_info["artist"], song_format
    )
    if WITH_RENAME == True and os.path.exists(dist_name):
        print("File %s exists, skip downloading" % (dist_name))
        return dist_name

    temp_download_path = os.path.join(
        dist_path, "{}-bite_rate-random_num.{}".format(song_id, song_format)
    )
    if WITH_RENAME == False and os.path.exists(temp_download_path):
        print("File %s exists, skip downloading" % (temp_download_path))
        return temp_download_path

    if not os.path.isdir(dist_path):
        os.mkdir(dist_path)

    download_contents = requests.get(url, headers=headers)
    if download_contents.url.endswith("404"):
        print(">>>> 404 is returned in download, song_id = %s" % (song_id))
        return None

    with open(temp_download_path, "wb") as ff:
        write_bytes = ff.write(download_contents.content)
        write_bytes_m = write_bytes / 1024 / 1024
        print("song id = %s, bytes write = %.2fM" % (song_id, write_bytes_m))

    if WITH_RENAME:
        dist_name = netease_rename.netease_cache_rename_single(
            song_id,
            temp_download_path,
            dist_path,
            KEEP_SOURCE=False,
            song_format=song_format,
        )
        return dist_name
    else:
        return temp_download_path


def netease_download_single_bit_rate(
    song_id, dist_path, bit_rate=320000, WITH_RENAME=True
):
    # bit_rate: {'MD 128k': 128000, 'HD 320k': 320000}
    song_download_url = "http://music.163.com/weapi/song/enhance/player/url?csrf_token="
    # params = {'ids': [song_id], 'br': bit_rate}
    csrf = ""
    params = {"ids": [song_id], "br": bit_rate, "csrf_token": csrf}

    data = encrypt.encrypted_request(params)
    resp = requests.post(song_download_url, data=data, timeout=30, headers=headers)
    resp_json = resp.json()
    download_url = resp_json["data"][0]["url"]

    if download_url == None:
        print(
            ">>>> download_url is None, maybe it is limited by copyright. song_id = %s"
            % (song_id)
        )
        return None

    return get_url_2_local_file(song_id, download_url, dist_path, WITH_RENAME)


def netease_download_single_outer(
    song_id, dist_path, bit_rate=320000, WITH_RENAME=True
):
    url_base = "http://music.163.com/song/media/outer/url?id={}.mp3"
    url = url_base.format(song_id)

    return get_url_2_local_file(song_id, url, dist_path, WITH_RENAME)


def netease_songid_2_baidu_single(song_id, strict_level=0):
    song_info, _ = netease_rename.detect_netease_music_name(song_id)
    song_name = song_info["title"]
    song_artist = song_info["artist"]

    url_suggestion = "http://sug.music.baidu.com/info/suggestion"
    if strict_level == 0:
        payload = {"word": song_artist + "+" + song_name, "version": "2", "from": "0"}
    elif strict_level == 1:
        payload = {"word": song_name + "+" + song_artist, "version": "2", "from": "0"}
    else:
        payload = {"word": song_name, "version": "2", "from": "0"}

    resp = requests.get(url_suggestion, params=payload)

    song_info = json.loads(resp.text, encoding="utf-8")
    if song_info is not None and "data" not in song_info:
        print(
            ">>>> song info not found, song_id = %s, song_name = %s"
            % (song_id, song_name)
        )
        return None

    song_id_baidu = song_info["data"]["song"][0]["songid"]
    song_name = song_info["data"]["song"][0]["songname"]
    song_artist = song_info["data"]["song"][0]["artistname"]
    print(
        ">>>> song_name = %s, artist = %s, song_id = %s, song_id_baidu = %s"
        % (song_name, song_artist, song_id, song_id_baidu)
    )

    return song_id_baidu, song_name, song_artist


def baidu_download_single_flac(song_id, dist_path, bit_rate=320000, WITH_RENAME=True):
    ret = netease_songid_2_baidu_single(song_id, strict_level=0)
    if ret == None:
        print(">>>> Baidu songid not found, song_id = %s" % (song_id))
        return None

    song_id_baidu, song_name, song_artist = ret

    url_base = "http://music.baidu.com/data/music/fmlink"
    payload = {"songIds": song_id_baidu, "type": "flac"}
    # payload = {'songIds': song_id_baidu}
    resp = requests.get(url_base, params=payload)
    resp_json = json.loads(resp.text, encoding="utf-8")
    if ("data" not in resp_json) or resp_json["data"] == "":
        print(">>>> No data found, song_id_baidu = %s" % (song_id_baidu))
        return None

    download_url = resp_json["data"]["songList"][0]["songLink"]
    if download_url == None or len(download_url) < 4:
        print(
            ">>>> download_url is None, maybe it is limited by copyright. song_id = %s"
            % (song_id)
        )
        return None
    song_format = resp_json["data"]["songList"][0]["format"]
    print("song_format = %s, url_download = %s" % (song_format, download_url))

    dist_name = netease_rename.generate_target_file_name(
        dist_path, song_name, song_artist, song_format
    )
    if os.path.exists(dist_name):
        print("File %s exists, skip downloading" % (dist_name))
        return dist_name

    if song_format == "mp3":
        dist_name_temp = get_url_2_local_file(
            song_id, download_url, dist_path, WITH_RENAME=True, song_format=song_format
        )
    else:
        dist_name_temp = get_url_2_local_file(
            song_id, download_url, dist_path, WITH_RENAME=False, song_format=song_format
        )
    os.rename(dist_name_temp, dist_name)

    return dist_name


def netease_download_list(
    song_list,
    dist_path,
    bit_rate=320000,
    WITH_RENAME=True,
    single_download_func=netease_download_single_bit_rate,
):
    song_not_downloaded = []
    song_downloaded = []
    for song_id in song_list:
        try:
            # ret = netease_download_single_bite_rate(song_id, dist_path, bit_rate, WITH_RENAME)
            ret = single_download_func(song_id, dist_path, bit_rate, WITH_RENAME)
        except KeyboardInterrupt as e:
            print("Keyboard Interrupt, exit now, e = %s" % (e))
            return None
        except:
            print("Some error heppens, song_id = %s" % (song_id))
            return None

        if ret == None:
            print(">>>> File NOT downloaded, song_id = %s" % (song_id))
            song_not_downloaded.append(song_id)
        else:
            print("dist_name = %s" % (ret))
            song_downloaded.append(song_id)
        print("")

    print("Song not downloaded:")
    for ss in netease_rename.detect_netease_music_name_list(song_not_downloaded):
        print("    %s: %s - %s" % (ss["song_id"], ss["artist"], ss["title"]))
    print()
    print("Song downloaded id: %s\n" % (song_downloaded))
    print("Song not downloaded id: %s\n" % (song_not_downloaded))
    print(
        "Downloaded = %d, NOT downloaded = %d\n"
        % (len(song_downloaded), len(song_not_downloaded))
    )

    return {
        "song_downloaded": song_downloaded,
        "song_not_downloaded": song_not_downloaded,
    }


def download_by_playlist(
    playlist_id,
    dist_path,
    bit_rate=320000,
    WITH_RENAME=True,
    single_download_func=netease_download_single_bit_rate,
):
    play_list = netease_parse_playlist_2_list(playlist_id)
    return netease_download_list(
        play_list, dist_path, bit_rate, WITH_RENAME, single_download_func
    )


def parse_arguments(argv):
    default_dist_path = "./netease_download_music"
    default_playlist_id = "101562485"

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=(
            "Download Netease song by <playlist> ID\n"
            "Also support specify a <song_id_list> to download\n"
            "Also support download Baidu flac music by <--baidu_flac>\n"
            "\n"
            "default dist path: %s\n"
            "default playlist id: %s" % (default_dist_path, default_playlist_id)
        ),
    )
    parser.add_argument(
        "-d",
        "--dist_path",
        type=str,
        help="Download output path",
        default=default_dist_path,
    )
    parser.add_argument(
        "-p",
        "--playlist",
        type=str,
        help="Playlist id to download",
        default=default_playlist_id,
    )

    parser.add_argument(
        "--outer",
        action="store_true",
        help="Downloading uses netease default output url",
    )
    parser.add_argument(
        "--bitrate",
        action="store_true",
        help="Downloading with bitrate=320k from netease, DEFAULT one",
    )
    parser.add_argument(
        "--baidu_flac",
        action="store_true",
        help="Downloading with flac format from baidu",
    )

    parser.add_argument(
        "--song_id_list",
        nargs="*",
        type=str,
        help="Specify song id list to download. Higher priority than playlist. Format 1 2 3 or 1, 2, 3",
    )

    args = parser.parse_args(argv)
    if args.song_id_list == None or len(args.song_id_list) == 0:
        args.song_id_list = netease_parse_playlist_2_list(args.playlist)
    else:
        args.song_id_list = [int(ss.replace(",", "")) for ss in args.song_id_list]

    if args.baidu_flac == True:
        args.single_download_func = baidu_download_single_flac
    elif args.outer == True:
        args.single_download_func = netease_download_single_outer
    else:
        args.single_download_func = netease_download_single_bit_rate

    return args


if __name__ == "__main__":
    args = parse_arguments(sys.argv[1:])
    netease_download_list(
        args.song_id_list,
        args.dist_path,
        single_download_func=args.single_download_func,
    )
elif __name__ == "__test__":
    playlist_id = "101562485"
    ll = netease_parse_playlist_2_list(playlist_id)
    ll = list(ll)
    song_not_found = []
    song_found = []
    for song_id in ll:
        ret = netease_songid_2_baidu_single(song_id, strict_level=2)
        if ret == None:
            song_not_found.append(song_id)
        else:
            song_found.append(song_id)

    for song_id in song_found:
        ss, _ = netease_rename.detect_netease_music_name(song_id)
        print("song_id = %s, song_info = %s" % (song_id, ss))

    ret = netease_download_playlist.download_by_playlist(
        playlist_id,
        dist_path="/home/leondgarse/Downloads/output_music_flac_2/",
        single_download_func=netease_download_playlist.baidu_download_single_flac,
    )
    list(netease_rename.detect_netease_music_name_list(ret["song_not_downloaded"]))

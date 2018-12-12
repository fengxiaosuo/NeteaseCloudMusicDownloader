#!/usr/bin/env python3

import os
import sys
import argparse
import netease_rename
import netease_download_playlist


def netease_refresh_by_playlist(source_path, dist_path, playlist_id, single_download_func, WITH_SIZE_CHECK=False):
    songlist = netease_download_playlist.netease_parse_playlist_2_list(playlist_id)
    netease_refresh_by_songlist(source_path, dist_path, songlist, single_download_func, WITH_SIZE_CHECK)


def netease_refresh_by_album(source_path, dist_path, album_id, single_download_func, WITH_SIZE_CHECK=False):
    songlist = netease_download_playlist.netease_parse_album_2_list(album_id)
    netease_refresh_by_songlist(source_path, dist_path, songlist, single_download_func, WITH_SIZE_CHECK)


def netease_refresh_by_songlist(source_path, dist_path, songlist, single_download_func, WITH_SIZE_CHECK=False):
    if not os.path.exists(dist_path):
        os.mkdir(dist_path)

    new_downloaded = []
    song_not_found = []
    for song_id in songlist:
        song_info, _ = netease_rename.detect_netease_music_name(song_id)
        source_path_file = netease_rename.generate_target_file_name(
            source_path, song_info["title"], song_info["artist"], song_format="mp3"
        )
        dist_path_file = netease_rename.generate_target_file_name(
            dist_path, song_info["title"], song_info["artist"], song_format="mp3"
        )

        if os.path.exists(dist_path_file):
            print("Dist file exists: %s" % (dist_path_file))
            temp_file_path = dist_path_file
        elif os.path.exists(source_path_file) and WITH_SIZE_CHECK == False:
            print("Source file exists: %s" % (source_path_file))
            temp_file_path = source_path_file
        else:
            print(
                "Dowload from netease, song_id = %s, title = %s, artist = %s"
                % (song_id, song_info["title"], song_info["artist"])
            )
            temp_file_path = single_download_func(song_id, dist_path, WITH_RENAME=False)
            new_downloaded.append(song_id)

            if temp_file_path != None and os.path.exists(source_path_file) and WITH_SIZE_CHECK == True:
                source_size = os.path.getsize(source_path_file)
                downloaded_size = os.path.getsize(temp_file_path)
                print(
                    "source_size = %.2fM, downloaded_size = %.2fM" % (source_size / 1024 / 1024, downloaded_size / 1024 / 1024)
                )
                if downloaded_size - source_size >= 500000:
                    print(">>>> Downloaded size is 500K bigger than source one")
                else:
                    new_downloaded.remove(song_id)
                    os.remove(temp_file_path)
                    temp_file_path = source_path_file
            elif temp_file_path == None and os.path.exists(source_path_file):
                new_downloaded.remove(song_id)
                temp_file_path = source_path_file

        if temp_file_path == None:
            print("Song not found, song_id = %s, title = %s, artist = %s" % (song_id, song_info["title"], song_info["artist"]))
            new_downloaded.remove(song_id)
            song_not_found.append(song_id)
        else:
            dist_path_file = netease_rename.netease_cache_rename_single(song_id, temp_file_path, dist_path, KEEP_SOURCE=False)
            print("Move %s to %s" % (temp_file_path, dist_path_file))

        print()

    print("New downloaded size = %d" % (len(new_downloaded)))
    for ss in netease_rename.detect_netease_music_name_list(new_downloaded):
        print("    %s: %s - %s" % (ss["song_id"], ss["artist"], ss["title"]))
    print()
    print("Song not found, size = %d:" % len(song_not_found))
    for ss in netease_rename.detect_netease_music_name_list(song_not_found):
        print("    %s: %s - %s" % (ss["song_id"], ss["artist"], ss["title"]))
    print()
    print("Song not found id: %s" % (song_not_found))
    return song_not_found


def parse_arguments(argv):
    default_dist_path = "./Netease_refreshed"
    default_playlist_id = "101562485"

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=(
            "Refresh local files in <source_path> by <playlist>, and save to <dist_path>\n"
            "1. Check song list in <playlist>\n"
            "2. If it is in <dist_path>, keep it\n"
            "3. If it is in <source_path>, move it to <dist_path>\n"
            "4. If it is not in local, download it from Netease, then move to <dist_path>\n"
            "All these steps will also update ID3 info and album cover images.\n"
            "Option <--with_size_check> will force check file size, and keep the bigger one\n"
            "\n"
            "default dist path: %s\n"
            "default playlist id: %s" % (default_dist_path, default_playlist_id)
        ),
    )
    parser.add_argument("source_path", type=str, help="Source folder contains music files")
    parser.add_argument("-p", "--playlist", type=str, help="Playlist id used to download", default=default_playlist_id)
    parser.add_argument("-a", "--album", type=str, help="Album id used to download", default=None)
    parser.add_argument("-d", "--dist_path", type=str, help="Dist output path", default=default_dist_path)
    parser.add_argument("--with_size_check", action="store_true", help="Enbale comparing source and downloaded file size")
    parser.add_argument("--outer", action="store_true", help="Downloading uses netease default output url, DEFAULT one")
    parser.add_argument("--bitrate", action="store_true", help="Downloading with bitrate=320k from netease")
    parser.add_argument("--baidu_flac", action="store_true", help="Downloading with flac format from baidu")

    args = parser.parse_args(argv)
    if args.baidu_flac == True:
        args.single_download_func = netease_download_playlist.baidu_download_single_flac
    elif args.bitrate == True:
        args.single_download_func = netease_download_playlist.netease_download_single_bit_rate
    else:
        args.single_download_func = netease_download_playlist.netease_download_single_outer

    return args


if __name__ == "__main__":
    args = parse_arguments(sys.argv[1:])
    if args.album != None:
        netease_refresh_by_album(args.source_path, args.dist_path, args.album, args.single_download_func, args.with_size_check)
    else:
        netease_refresh_by_playlist(
            args.source_path, args.dist_path, args.playlist, args.single_download_func, args.with_size_check
        )

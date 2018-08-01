# NeteaseCloudMusicDownloader
***

# 目录
  <!-- TOC depthFrom:1 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 -->

  - [NeteaseCloudMusicDownloader](#neteasecloudmusicdownloader)
  - [目录](#目录)
  - [依赖](#依赖)
  - [netease rename 网易云音乐缓存重命名](#netease-rename-网易云音乐缓存重命名)
  	- [功能](#功能)
  	- [使用说明示例](#使用说明示例)
  	- [参数](#参数)
  - [netease download playlist 网易云音乐下载播放列表](#netease-download-playlist-网易云音乐下载播放列表)
  	- [功能](#功能)
  	- [使用说明示例](#使用说明示例)
  	- [参数](#参数)
  - [netease refresh by playlist 根据播放列表更新本地文件](#netease-refresh-by-playlist-根据播放列表更新本地文件)
  	- [功能](#功能)
  	- [使用说明示例](#使用说明示例)
  	- [参数](#参数)

  <!-- /TOC -->
# 依赖
  - **eyed3** mp3 文件属性赋值，如 title / artist / album / album_artist
    ```shell
    $ pip install eyed3
    ```
  - **requests** 网页请求
    ```shell
    $ pip install requests
    ```
  - **shutil** 文件复制
    ```shell
    $ pip install shutil
    ```
  - **Crypto** 加密
    ```shell
    $ pip install Crypto
    ```
***

# netease rename 网易云音乐缓存重命名
## 功能
  - 重命名 mp3 文件，查找 song id 对应的 `歌手名` 与 `歌曲名`，并将文件重命名为 `歌手名 - 歌曲名.mp3`
    ```md
    From: source path/<song id>-<bite rate>-<random number>.mp3
    To: dist path/<artist name> - <song title>.mp3
    ```
## 使用说明示例
  - 在 Ubuntu 上使用网易云音乐的客户端，其缓存直接是 mp3 文件，缓存在 `~/.cache/netease-cloud-music/CachedSongs/`
    ```shell
    $ ls ~/.cache/netease-cloud-music/CachedSongs/ -1
    1609689-320-b70d1d38edd3f443bc503f592fc440ed.mp3
    25638306-320-3d42ddad5384518bbbf8bc68fff4cdfa.mp3
    4254253-128-1fb4ae7055ea4ceb36862f6228e61aa4.mp3
    441116287-128-0d15579de47acbe4c8177e54ba43bf4b.mp3
    ```
  - 因此主要需要的是重命名，使用如下
    ```shell
    $ python netease_rename.py
    source = ~/.cache/netease-cloud-music/CachedSongs, dist = ./output_music
    song_id = 25638306, tt.tag title = ありがとう…, artist = KOKIA, album = ありがとう…, album_artist = KOKIA
    song_id = 441116287, tt.tag title = 茜さす, artist = Aimer, album = 茜さす/everlasting snow, album_artist = Aimer
    song_id = 4254253, tt.tag title = Mustang cabriolet, artist = Paris Brune, album = L’œil du cyclone, album_artist = Paris Brune
    song_id = 1609689, tt.tag title = Vale Of Tears, artist = Jay Clifford, album = Silver Tomb For The Kingfisher, album_artist = Jay Clifford
    ```
  - 输出
    ```shell
    $ ls ./output_music/ -1
    'Aimer - 茜さす.mp3'
    'Jay Clifford - Vale Of Tears.mp3'
    'KOKIA - ありがとう….mp3'
    'Paris Brune - Mustang cabriolet.mp3'
    ```
## 参数
  - `--dist_path` 输出路径，默认 `./output_music`
  - `--source_path` 输入文件夹路径，缓存文件地址，默认 `$HOME/.cache/netease-cloud-music/CachedSongs`
  - `--remove_source` 指定删除源文件，默认保留源文件
  - `--help` 帮助信息
  - 示例
    ```shell
    # 帮助信息
    ./netease_rename.py -h
    # 指定其他输出路径
    ./netease_rename.py -d ~/output_music
    # 指定其他输入路径，并指定删除源文件
    ./netease_rename.py -s ./CachedSongs --remove_source
    ```
***

# netease download playlist 网易云音乐下载播放列表
## 功能
  - 根据 playlist 下载音乐文件到本地，如果本地指定的文件夹中存在同名文件则跳过
  - 支持三种不同的下载方式
    ```python
    # outer url
    "http://music.163.com/song/media/outer/url?id={song id}.mp3"
    # bitrate url，默认方式
    "http://music.163.com/weapi/song/enhance/player/url?csrf_token=&ids={song id}&br={bit rate}"
    # Baidu flac url
    "http://music.baidu.com/data/music/fmlink?songIds={song id}&type=flac"
    ```
  - 支持指定 <song id list> 下载，如果指定了，则优先级高于 playlist
## 使用说明示例
  - **开始下载**
    ```shell
    $ ./netease_download_playlist.py -p 101562485 -d ~/Downloads/netease

    ...
    song id = 22701801, bytes write = 9.59M
    song_id = 22701801, tt.tag {title = ありがとう..., artist = KOKIA, album = Complete collection 1998-1999, album_artist = KOKIA}
    dist_name = /home/leondgarse/Downloads/netease/KOKIA - ありがとう....mp3
    ...
    song id = 441116287, bytes write = 5.04M
    song_id = 441116287, tt.tag {title = 茜さす, artist = Aimer, album = 茜さす/everlasting snow, album_artist = Aimer}
    dist_name = /home/leondgarse/Downloads/netease/Aimer - 茜さす.mp3
    ...
    ```
  - **下载失败的文件**
    ```shell
    >>>> download_url is None, maybe it is limited by copyright. song_id = 497762
    >>>> File NOT downloaded, song_id = 497762
    ```
  - **本地已有的文件**
    ```shell
    File /home/leondgarse/Downloads/netease/Wiz Khalifa - See You Again.mp3 exists, skip downloading
    dist_name = /home/leondgarse/Downloads/netease/Wiz Khalifa - See You Again.mp3

    File /home/leondgarse/Downloads/netease/Charlie Puth - Need You Now.mp3 exists, skip downloading
    dist_name = /home/leondgarse/Downloads/netease/Charlie Puth - Need You Now.mp3
    ```
  - **下载完成**
    ```shell
    Song not downloaded:
        497762: スガシカオ - 19才
        27533158: Kari Kimmel - Fingerprints

    Song downloaded id: [287025, 29481242, ...]

    Song not downloaded id: [497762, 27533158, ...]

    Downloaded = 190, NOT downloaded = 14
    ```
## 参数
  - `-h, --help` 帮助信息
  - `-d DIST_PATH, --dist_path DIST_PATH` 下载的输出路径，默认 `./netease_download_music`
  - `-p PLAYLIST, --playlist PLAYLIST` 下载的播放列表，默认 `101562485`
  - `--outer` 指定使用 outer url 方式下载
  - `--bitrate` 指定使用 bitrate url 方式下载，可以指定 bitrate=320k，默认方式
  - `--baidu_flac` 指定使用 Baidu flac 方式下载，可以下载 flac 格式的无损音乐，出错率高
  - `--song_id_list [SONG_ID_LIST [SONG_ID_LIST ...]]` 指定一个 <song id list> 下载，而不使用 playlist，格式可以是 `1 2 3` 或 `1, 2, 3`
  - 示例
    ```shell
    # 帮助信息
    ./netease_download_playlist.py -h
    # 指定要下载的 playlist
    ./netease_download_playlist.py -p 123123123
    # 指定其他输出路径
    ./netease_download_playlist.py -d ~/Music/netease_download_music
    # 指定其他下载方式
    ./netease_download_playlist.py --baidu_flac -p 123123123 -d ~/Music/netease_flac
    # 指定  <song id list>
    ./netease_download_playlist.py --song_id_list 123 456 798, 1234, 4567, 7980 --outer -d ~/Music/netease_outer
    ```
***

# netease refresh by playlist 根据播放列表更新本地文件
## 功能
  - 根据播放列表 <playlist> 更新本地文件 <source_path>，并将文件移动到 <dist_path>
    - 检查播放列表中的音乐文件
    - 如果 <dist_path> 中存在该文件，保留
    - 如果 <source_path> 中存在该文件，移动到 <dist_path>
    - 如果本地都不存在，从 Netease 下载并移动到 <dist_path>
  - 所有文件都会更新 ID3 信息，并重新下载专辑封面图片
  - 选项 <--with_size_check> 指定对比文件大小，如果下载的文件大小大于本地文件 500K，则保留下载的文件
## 使用说明示例
  - **开始更新**
    ```shell
    $ ./netease_refresh_by_playlist.py ~/Downloads/netease/ -p 101562485 -d ~/Downloads/netease_refreshed
    ...
    Source file exists: /home/leondgarse/Downloads/netease/KOKIA - ありがとう....mp3
    song_id = 22701801, tt.tag {title = ありがとう..., artist = KOKIA, album = Complete collection 1998-1999, album_artist = KOKIA}
    Move /home/leondgarse/Downloads/netease/KOKIA - ありがとう....mp3 to /home/leondgarse/Downloads/netease_refreshed/KOKIA - ありがとう....mp3
    ...
    Source file exists: /home/leondgarse/Downloads/netease/Aimer - 茜さす.mp3
    song_id = 441116287, tt.tag {title = 茜さす, artist = Aimer, album = 茜さす/everlasting snow, album_artist = Aimer}
    Move /home/leondgarse/Downloads/netease/Aimer - 茜さす.mp3 to /home/leondgarse/Downloads/netease_refreshed/Aimer - 茜さす.mp3
    ...
    ```
  - **重新下载的文件**
    ```shell
    Dowload from netease, song_id = 286970, title = 愚人的国度, artist = 孙燕姿
    song id = 286970, bytes write = 3.80M
    song_id = 286970, tt.tag {title = 愚人的国度, artist = 孙燕姿, album = 是时候, album_artist = 孙燕姿}
    Move /home/leondgarse/Downloads/netease_refreshed/286970-bite_rate-random_num.mp3 to /home/leondgarse/Downloads/netease_refreshed/孙燕姿 - 愚人的国度.mp3
    ```
  - **本地没有且下载失败的文件**
    ```shell
    Dowload from netease, song_id = 497762, title = 19才, artist = スガシカオ
    >>>> download_url is None, maybe it is limited by copyright. song_id = 497762
    Song not found, song_id = 497762, title = 19才, artist = スガシカオ
    ```
  - **更新完成**
    ```shell
    New downloaded size = 15
        286970: 孙燕姿 - 愚人的国度
        497762: スガシカオ - 19才
        27533158: Kari Kimmel - Fingerprints
        ...

    New downloaded id: [286970, 497762, 27533158, ...]
    ```
## 参数
  - `source_path` 包含音乐文件的源文件地址，必须参数
  - `-h, --help` 帮助信息
  - `-p PLAYLIST, --playlist PLAYLIST` 播放列表 ID，默认 `101562485`
  - `-d DIST_PATH, --dist_path DIST_PATH` 输出路径，默认 `./Netease_refreshed`
  - `--with_size_check` 指定对比文件大小，如果下载的文件大小大于本地文件 500K，则保留下载的文件
  - 示例
    ```shell
    ~/Downloads/netease/ -p 101562485 -d ~/Downloads/netease_refreshed
    # 帮助信息
    ./netease_refresh_by_playlist.py -h
    # 指定要下载的 playlist
    ./netease_refresh_by_playlist.py ~/Downloads/netease/ -p 101562485
    # 指定其他输出路径
    ./netease_refresh_by_playlist.py ~/Downloads/netease/ -p 101562485 -d ~/Downloads/netease_refreshed
    # 指定对比文件大小
    ./netease_refresh_by_playlist.py ~/Downloads/netease/ -p 101562485 -d ~/Downloads/netease_refreshed --with_size_check
    ```
***

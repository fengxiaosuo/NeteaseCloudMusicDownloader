# NeteaseCloudMusicDownloader
***

- 似乎由于 api 接口改版，目前获取播放列表失败。。

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
    # outer url，默认方式
    "http://music.163.com/song/media/outer/url?id={song id}.mp3"
    # bitrate url
    "http://music.163.com/weapi/song/enhance/player/url?csrf_token=&ids={song id}&br={bit rate}"
    # Baidu flac url
    "http://music.baidu.com/data/music/fmlink?songIds={song id}&type=flac"
    ```
  - 支持指定 `<song id list>` 下载，如果指定了，则优先级高于 playlist
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
  - `--outer` 指定使用 outer url 方式下载，默认方式
  - `--bitrate` 指定使用 bitrate url 方式下载，可以指定 bitrate=320k，容易检测为 cheating
  - `--baidu_flac` 指定使用 Baidu flac 方式下载，可以下载 flac 格式的无损音乐，出错率高
  - `--song_id_list [SONG_ID_LIST [SONG_ID_LIST ...]]` 指定一个 song id list 下载，而不使用 playlist，格式可以是 `1 2 3` 或 `1, 2, 3`
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
  - 根据播放列表 `<playlist>` 更新本地文件 `<source_path>`，并将文件移动到 `<dist_path>`
    - 检查播放列表中的音乐文件
    - 如果 `<dist_path>` 中存在该文件，保留
    - 如果 `<source_path>` 中存在该文件，移动到 `<dist_path>`
    - 如果本地都不存在，从 Netease 下载并移动到 `<dist_path>`
  - 所有文件都会更新 ID3 信息，并重新下载专辑封面图片
  - 选项 `<--with_size_check>` 指定对比文件大小，如果下载的文件大小大于本地文件 **500K**，则保留下载的文件
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
  - `--outer` 指定使用 outer url 方式下载，默认方式
  - `--bitrate` 指定使用 bitrate url 方式下载，可以指定 bitrate=320k，容易检测为 cheating
  - `--baidu_flac` 指定使用 Baidu flac 方式下载，可以下载 flac 格式的无损音乐，出错率高
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

# Test
## Post request
  ```html
  Frame 237: 67 bytes on wire (536 bits), 67 bytes captured (536 bits) on interface 0
  Ethernet II, Src: IntelCor_e0:ef:34 (b4:d5:bd:e0:ef:34), Dst: Tp-LinkT_88:15:0d (8c:a6:df:88:15:0d)
  Internet Protocol Version 4, Src: 192.168.1.118, Dst: 223.252.199.67
  Transmission Control Protocol, Src Port: 51802, Dst Port: 80, Seq: 2866, Ack: 437, Len: 1
  [2 Reassembled TCP Segments (1369 bytes): #236(1368), #237(1)]
  Hypertext Transfer Protocol
      POST /api/linux/forward HTTP/1.1\r\n
          [Expert Info (Chat/Sequence): POST /api/linux/forward HTTP/1.1\r\n]
          Request Method: POST
          Request URI: /api/linux/forward
          Request Version: HTTP/1.1
      Host: music.163.com\r\n
      Connection: keep-alive\r\n
      Content-Length: 264\r\n
      User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36\r\n
      Origin: orpheus://orpheus\r\n
      Content-Type: application/x-www-form-urlencoded\r\n
      Accept: */*\r\n
      Accept-Encoding: gzip, deflate\r\n
      Accept-Language: en-US,en;q=0.8\r\n
       [truncated]Cookie: os=linux; deviceId=976f9ea6db880ea1d8cc62ebb0c8100a46319070f5fbd776ce32; osver=Ubuntu%2018.04.1%20LTS; appver=1.1.0.1232; MUSIC_A=17a0474dca5c39776f451b327cba6db76bbf9da46d32bdb4ad83447d6429bc01d5bd7e632f6b9f4e3d3ab44b4
      \r\n
      [Full request URI: http://music.163.com/api/linux/forward]
      [HTTP request 2/3]
      [Prev request in frame: 229]
      [Response in frame: 240]
      [Next request in frame: 1920]
      File Data: 264 bytes
  HTML Form URL Encoded: application/x-www-form-urlencoded
      Form item: "eparams" = "045913148E5D4B33D53D16D283F3C3445BCA8A188E1BE398DB4C9A3FC117E19CFD5383E018356CEB3F0AE94452892D4ED77FA1307DCE569066821F538183EC9A11BA253DED5B5D7883C32F6A60F50658C227FE4CC1F2076243736E2A36B635D0E8864A120B597EE567CEB56
          Key: eparams
          Value [truncated]: 045913148E5D4B33D53D16D283F3C3445BCA8A188E1BE398DB4C9A3FC117E19CFD5383E018356CEB3F0AE94452892D4ED77FA1307DCE569066821F538183EC9A11BA253DED5B5D7883C32F6A60F50658C227FE4CC1F2076243736E2A36B635D0E8864A120B597EE567CEB5693CCE
  ```
## 200 OK
  ```html
  Frame 240: 86 bytes on wire (688 bits), 86 bytes captured (688 bits) on interface 0
  Ethernet II, Src: Tp-LinkT_88:15:0d (8c:a6:df:88:15:0d), Dst: IntelCor_e0:ef:34 (b4:d5:bd:e0:ef:34)
  Internet Protocol Version 4, Src: 223.252.199.67, Dst: 192.168.1.118
  Transmission Control Protocol, Src Port: 80, Dst Port: 51802, Seq: 1052, Ack: 2867, Len: 20
  [2 Reassembled TCP Segments (635 bytes): #239(615), #240(20)]
  Hypertext Transfer Protocol
      HTTP/1.1 200 OK\r\n
          [Expert Info (Chat/Sequence): HTTP/1.1 200 OK\r\n]
          Request Version: HTTP/1.1
          Status Code: 200
          [Status Code Description: OK]
          Response Phrase: OK
      Server: nginx\r\n
      Date: Tue, 07 Aug 2018 07:01:31 GMT\r\n
      Content-Type: text/plain;charset=UTF-8\r\n
      Transfer-Encoding: chunked\r\n
      Connection: keep-alive\r\n
      Vary: Accept-Encoding\r\n
      Cache-Control: no-store\r\n
      Pragrma: no-cache\r\n
      Expires: Thu, 01 Jan 1970 00:00:00 GMT\r\n
      Cache-Control: no-cache\r\n
      X-Via: MusicServer\r\n
      X-From-Src: 223.80.99.37\r\n
      Content-Encoding: gzip\r\n
      \r\n
      [HTTP response 2/3]
      [Time since request: 0.050092533 seconds]
      [Prev request in frame: 229]
      [Prev response in frame: 234]
      [Request in frame: 237]
      [Next request in frame: 1920]
      [Next response in frame: 1937]
      HTTP chunked response
      Content-encoded entity body (gzip): 254 bytes -> 350 bytes
      File Data: 350 bytes
  Line-based text data: text/plain
       [truncated]{"data":{"id":534568536,"url":"http://m8.music.126.net/20180807152631/e382b3cde7a3e1199debd4ce4a0105a1/ymusic/e90d/6ec2/4ce5/20c413f24f798d65deea22da9d371ccb.mp3","br":320000,"size":10603668,"md5":"20c413f24f798d65deea22da9d371
  ```
## Python test
  ```py
  import netease_rename
  import netease_download_playlist

  aa = netease_download_playlist.netease_parse_playlist_2_list(playlist_id=101562485)
  bb = [ii for ii in netease_rename.detect_netease_music_name_list(aa) if ii['title'] == '简爱']
  bb = [ii for ii in netease_rename.detect_netease_music_name_list(aa) if ii['artist'] == '孙燕姿']
  song_id = bb[0]['song_id']

  netease_download_playlist.netease_download_single_bit_rate(song_id=song_id, SIZE_ONLY=True)
  netease_download_playlist.netease_download_single_bit_rate(song_id=30431376, dist_path='./')

  aa = netease_download_playlist.netease_parse_playlist_2_list(playlist_id=101562485)
  dd = DataFrame(netease_rename.detect_netease_music_name_list(aa))
  print(dd.song_id.min(), dd.song_id.max())
  # 64634 1302261203
  
  print(dd.artist.value_counts().head(9))
  # 孙燕姿                 8
  # 曹方                  7
  # 陈奕迅                 4
  # Garou               4
  # 莫文蔚                 4
  # 郑欣宜                 3
  # 陈粒                  3
  # 金海心                 3
  # Rachael Yamagata    3
  # Name: artist, dtype: int64
  ```
  ```python
  # request [http://music.163.com/api/linux/forward] time is 5954
  # {"type":"song","id":534568536,"resolution":320,"seq":20502}

  headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-GB,en;q=0.5",
    "Connection": "keep-alive",
    "Host": "api.imjad.cn",
    "Referer": "https://api.imjad.cn/cloudmusic.md",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0"
  }

  headers = {
    "Host": "music.163.com",
    "Connection": "keep-alive",
    "Content-Length": "264",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
    "Origin": "orpheus://orpheus",
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.8"
  }

  url_base = "http://music.163.com/api/linux/forward"
  data = {"eparams": "045913148E5D4B33D53D16D283F3C3445BCA8A188E1BE398DB4C9A3FC117E19CFD5383E018356CEB3F0AE94452892D4ED77FA1307DCE569066821F538183EC9A11BA253DED5B5D7883C32F6A60F50658C227FE4CC1F2076243736E2A36B635D0E8864A120B597EE567CEB5693CCE750C7EF54E238436BDE0CA8F376126AA1104"}

  resp = requests.post(url_base, data=data, headers=headers)
  resp.json()['data']['size'] / 1024 / 1024

  uur = resp.json()["data"]["url"]
  resp = requests.get(uur)
  len(resp.content) / 1024 / 1024
  ```
  ```python
  def encrypted_id(id):
      byte1 = bytearray('3go8&$8*3*3h0k(2)2', 'utf8')
      byte2 = bytearray(id, 'utf8')
      byte1_len = len(byte1)
      for i in xrange(len(byte2)):
          byte2[i] = byte2[i]^byte1[i%byte1_len]
      m = md5()
      m.update(byte2)
      result = m.digest().encode('base64')[:-1]
      result = result.replace('/', '_')
      result = result.replace('+', '-')
      return result

  def save_song_to_disk(song, folder):
      name = song['name']
      fpath = os.path.join(folder, name+'.mp3')
      if os.path.exists(fpath):
          return

      song_dfsId = str(song['bMusic']['dfsId'])
      url = 'http://m%d.music.126.net/%s/%s.mp3' % (random.randrange(1, 3), encrypted_id(song_dfsId), song_dfsId)
      #print '%s\t%s' % (url, name)
      #return
      resp = urllib2.urlopen(url)
      data = resp.read()
      f = open(fpath, 'wb')
      f.write(data)
      f.close()
  ```
  ```python
  # 获取高音质mp3 url
  def geturl(song):
      quality = Config().get_item('music_quality')
      if song['hMusic'] and quality <= 0:
          music = song['hMusic']
          quality = 'HD'
          play_time = str(music['playTime'])
      elif song['mMusic'] and quality <= 1:
          music = song['mMusic']
          quality = 'MD'
          play_time = str(music['playTime'])
      elif song['lMusic'] and quality <= 2:
          music = song['lMusic']
          quality = 'LD'
          play_time = str(music['playTime'])
      else:
          play_time = 0
          return song['mp3Url'], '', play_time
      quality = quality + ' {0}k'.format(music['bitrate'] // 1000)
      song_id = str(music['dfsId'])
      enc_id = encrypted_id(song_id)
      url = 'http://m%s.music.126.net/%s/%s.mp3' % (2,
                                                    enc_id, song_id)
  return url, quality, play_time
  ```
  ```python
  'https://api.imjad.cn/cloudmusic?type=song&id={}&br={}'.format(song_id, br)
  ```

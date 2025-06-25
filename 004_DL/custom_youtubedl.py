import os
from yt_dlp import YoutubeDL

# ffmpegのbinフォルダを環境変数に登録する
# 既に環境変数に登録済みならこの処理は不要
path = r'C:\Users\241822\Desktop\Tools\ffmpeg\bin'
os.environ['PATH'] +=  '' if path in os.environ['PATH'] else ';' + path

#オプションを指定（最高画質の動画と最高音質の音声を取り出し結合するためのオプション）
option = {
        'format' : 'bestvideo+bestaudio/best'
    }

ydl = YoutubeDL(option)

url = input('URL:')
result = ydl.download([url])

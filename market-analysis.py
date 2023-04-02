#!pip install git+https://github.com/openai/whisper.git -q
#!pip install pytube -q
#!pip install mplfinance -q
import whisper
from pytube import YouTube
import datetime
import pandas as pd
import mplfinance as mpf

model = whisper.load_model('small')
youtube_video_url = "https://www.youtube.com/watch?v=5NfD8UTPKsA"
youtube_video = YouTube(youtube_video_url)
for stream in youtube_video.streams:
  print(stream)
streams = youtube_video.streams.filter(only_audio=True) #filter only audio streams
stream = streams.first()
stream.download(filename='fed_meeting.mp4')
!ffmpeg -ss 2000 -i fed_meeting.mp4 -t 5000 audio_trim.mp4


# save a timestamp before transcription
t1 = datetime.datetime.now()
print(f"started at {t1}")
# do the transcription
output = model.transcribe("audio_trimmed.mp4")
# show time elapsed after transcription is complete.
t2 = datetime.datetime.now()
print(f"ended at {t2}")
print(f"time elapsed: {t2 - t1}")
output['text'] #transcription complete output
for segment in output['segments']:
  print(segment)
  second = int(segment['start'])
  second = second - (second % 5)
  print(second)
sp = pd.read_csv("sp500.csv")
for segment in output['segments']:
   second = int(segment['start'])
   second = second - (second % 5)
   sp.loc[second / 5, 'text'] = segment['text']
sp['percent'] = ((sp['close'] - sp['open']) / sp['open']) * 100
downmoves = sp[sp.percent < -0.2]
df = sp
df.index = pd.DatetimeIndex(df['date'])

mpf.plot(df['2022-12-02 14:36':'2022-12-02 14:39'],type='candle')


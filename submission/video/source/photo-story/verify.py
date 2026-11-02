#!/usr/bin/env python3
"""Validate only the new film: timing, continuous captions, decode, audio and photo motion."""
import argparse,subprocess,re,json,hashlib
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--baseline',type=Path,help='Previously verified movie whose unchanged intro will be compared');p.add_argument('--ffmpeg',required=True);a=p.parse_args();ff=a.ffmpeg
out=Path(__file__).resolve().parents[2];movie=out/'village-jobs-photo-story-fixed-en.mp4';folder=Path(__file__).resolve().parent
info=subprocess.run([ff,'-hide_banner','-i',str(movie)],capture_output=True,text=True).stderr
assert 'Audio:' not in info, 'Unexpected audio stream'
assert '1920x1080' in info and 'h264' in info, info
m=re.search(r'Duration: (\d+):(\d+):(\d+\.\d+)',info);assert m,info
duration=int(m[1])*3600+int(m[2])*60+float(m[3]);assert duration<=180
subprocess.run([ff,'-v','error','-i',str(movie),'-f','null','-'],check=True,capture_output=True)
srt=(out/'village-jobs-photo-story-fixed.en.srt').read_text();assert srt.isascii()
def sec(t):
 h,m,s=t.split(':');return int(h)*3600+int(m)*60+float(s.replace(',','.'))
ranges=[(sec(x),sec(y)) for x,y in re.findall(r'([\d:,]+) --> ([\d:,]+)',srt)]
assert len(ranges)==30 and ranges[0][0]==0
assert abs(ranges[-1][1]-duration)<.04
assert all(abs(ranges[i][1]-ranges[i+1][0])<.001 for i in range(len(ranges)-1)), 'Caption gap or overlap'
# Compare only the photograph area, excluding titles/captions, within each shot.
def frame(t):
 return subprocess.run([ff,'-v','error','-ss',str(t),'-i',str(movie),'-frames:v','1','-vf','crop=1920:880:0:50,scale=160:90,format=gray','-f','rawvideo','-'],capture_output=True,check=True).stdout
motion=[];intro_check='not requested'
if a.baseline:
 previous=json.loads((folder/'verification.json').read_text())
 assert hashlib.sha256(a.baseline.read_bytes()).hexdigest()==previous['sha256'], 'Baseline must match the previously verified movie'
 def intro_hash(movie_path):
  return subprocess.run([ff,'-v','error','-i',str(movie_path),'-frames:v','972','-vf','format=yuv420p','-an','-f','hash','-hash','sha256','-'],capture_output=True,check=True).stdout.strip().decode()
 assert intro_hash(a.baseline)==intro_hash(movie), 'Photo intro changed'
 motion=previous['photoMotion'];intro_check='First 972 decoded frames exactly match the previously verified movie'
else:
 for i in range(8):
  x,y=frame(i*4+.8),frame(i*4+2.8);assert len(x)==len(y)==14400
  delta=sum(abs(v-w) for v,w in zip(x,y))/len(x);assert delta>.3,(i,delta)
  motion.append({'shot':i+1,'meanPixelDifference':round(delta,3)})
caption_blocks=srt.strip().split('\n\n')
max_cps=max(len(' '.join(block.splitlines()[2:]))/(end-start) for block,(start,end) in zip(caption_blocks,ranges))
assert max_cps<=22, f'Caption too fast: {max_cps:.1f} characters/second'
photos=json.loads((folder/'photos.json').read_text())
provenance=[]
for s in photos:
 file=out/'raw'/'photo-story'/s['file'];assert file.exists()
 provenance.append({'file':'raw/photo-story/'+s['file'],'sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'model':'muse-image-1.0','fictional':True})
result={'durationSeconds':duration,'resolution':'1920x1080','videoCodec':'H.264','audioStreams':0,'generatedPhotos':8,'photoStorySeconds':32.4,'captionLanguage':'English','captionCues':30,'captionCoverage':'continuous from 0 to end, no timing gaps or overlaps','fullDecode':'passed','photoMotion':motion,'introUnchanged':intro_check,'maxCaptionCharactersPerSecond':round(max_cps,2),'photoTransitions':'seven 0.4-second cross-dissolves','appSource':'five existing native browser MP4 recordings; edited real interactions','generation':'Meta Muse Image; eight successful image outputs; two initial HTTP 400 size-validation failures','estimatedNewImageCostUsd':.08,'costNote':'Published unit-price estimate, not a verified billing statement; no external paid services','visualReview':'Pending final key-frame review','appDemoSeconds':80,'previousAppDemoSeconds':137,'newGenerationCallsThisRevision':0,'incrementalGenerationCostThisRevisionUsd':0,'bytes':movie.stat().st_size,'sha256':hashlib.sha256(movie.read_bytes()).hexdigest(),'assets':provenance,'publicUpload':'not performed'}
(folder/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['durationSeconds','audioStreams','generatedPhotos','captionCues','captionCoverage','bytes']}))

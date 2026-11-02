#!/usr/bin/env python3
"""Edit native browser MP4 recordings; never build UI footage from still images.
Usage: python3 render.py --raw-dir /tmp/village-film --ffmpeg /path/to/ffmpeg
Meta-generated fictional Korean photo story, then actual native product video.
Smooth pan/zoom and dissolves; continuous English captions; no audio. Rendering makes no API calls.
"""
import argparse,json,subprocess,re,wave,shutil
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--reuse-intro',action='store_true',help='Reuse the unchanged existing photo-story intro');p.add_argument('--only',help='Render only these comma-separated scene ids, then rebuild the master');p.add_argument('--raw-dir',type=Path,required=True);p.add_argument('--ffmpeg',default=shutil.which('ffmpeg'));p.add_argument('--output-dir',type=Path,default=Path(__file__).resolve().parents[2]);args=p.parse_args()
assert args.ffmpeg,'FFmpeg is required';ff=args.ffmpeg;raw=args.raw_dir;out=args.output_dir;work=raw/'edit-photo-story';work.mkdir(exist_ok=True);out.mkdir(exist_ok=True)
scenes=json.loads(Path(__file__).with_name('storyboard.json').read_text())
def run(cmd):
 result=subprocess.run(cmd,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
 if result.returncode:print(result.stderr.decode()[-6000:]);result.check_returncode()
def ass_time(t):
 c=round(t*100);return f'{c//360000}:{c//6000%60:02}:{c//100%60:02}.{c%100:02}'
def srt_time(t):
 m=round(t*1000);return f'{m//3600000:02}:{m//60000%60:02}:{m//1000%60:02},{m%1000:03}'
def ass(text):return text.replace('\\','\\\\').replace('\n',r'\N')
header='''[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Caption,Arial,36,&H00FFFFFF,&H00FFFFFF,&H0013261A,&H00000000,0,0,0,0,100,100,0,0,1,0,0,2,90,90,22,1
Style: Label,Arial,22,&H00D7E7D9,&H00FFFFFF,&H0013261A,&H00000000,0,0,0,0,100,100,1,0,1,0,0,7,160,90,12,1
Style: Notice,Arial,20,&H00FFFFFF,&H00FFFFFF,&H0013261A,&H00000000,0,0,0,0,100,100,0,0,1,1,0,7,60,60,70,1
Style: Title,Arial,68,&H00FFFFFF,&H00FFFFFF,&H0013261A,&H00000000,-1,0,0,0,100,100,0,0,1,0,0,5,90,90,40,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
'''
photos=json.loads(Path(__file__).with_name('photos.json').read_text())
photo_dir=out/'raw'/'photo-story'
photo_duration=4.4;overlap=.4;intro_duration=32.4
photo_clips=[]
for i,s in enumerate(photos):
 clip=work/(s['id']+'.mp4');photo_clips.append(clip)
 # Render at double resolution before the moving crop to avoid one-pixel stepping.
 ease="(3*pow(on/131,2)-2*pow(on/131,3))"
 z=f"1.03+0.07*{ease}" if i%2==0 else f"1.10-0.07*{ease}"
 x="iw/2-iw/zoom/2" if i%3==0 else f"(iw-iw/zoom)*({'.25+.5' if i%3==1 else '.75-.5'}*{ease})"
 vf=f"scale=3840:2160:force_original_aspect_ratio=increase,crop=3840:2160,zoompan=z='{z}':x='{x}':y='ih/2-ih/zoom/2':d=132:s=1920x1080:fps=30,setsar=1,format=yuv420p"
 if not clip.exists():run([ff,'-v','error','-i',str(photo_dir/s['file']),'-vf',vf,'-frames:v','132','-an','-c:v','libx264','-preset','fast','-crf','19','-y',str(clip)])
 print('photo motion rendered:',s['id'],flush=True)
intro_ass=work/'intro.ass';intro_lines=[header]
intro_lines.append(f'Dialogue: 1,0:00:00.00,{ass_time(intro_duration)},Label,,0,0,0,,VILLAGE JOBS / WORK CLOSE TO HOME\n')
intro_lines.append(f'Dialogue: 1,0:00:00.00,{ass_time(intro_duration)},Notice,,0,0,0,,{{\\an9\\pos(1760,15)\\fs18}}AI-generated photos / fictional scenario\n')
global_cues=[];timeline=[]
for i,s in enumerate(photos):
 start=i*4.;end=(i+1)*4. if i<7 else intro_duration
 intro_lines.append(f'Dialogue: 3,{ass_time(start)},{ass_time(end)},Caption,,0,0,0,,{ass(s["caption"])}\n')
 global_cues.append((start,end,s['caption']))
 timeline.append({'id':s['id'],'type':'animated-photo','start':start,'duration':end-start,'file':s['file'],'caption':s['caption'],'motion':'eased zoom and pan; 0.4-second cross-dissolve'})
intro_ass.write_text(''.join(intro_lines))
cmd=[ff,'-v','error','-filter_complex_threads','1']
for clip in photo_clips:cmd+=['-i',str(clip)]
filters=[];last='0:v'
for i in range(1,len(photo_clips)):
 tag=f'fade{i}'
 filters.append(f'[{last}][{i}:v]xfade=transition=fade:duration=0.4:offset={i*4.}[{tag}]');last=tag
filters.append(f'[{last}]drawbox=x=0:y=0:w=iw:h=46:color=0x13261a@0.92:t=fill,drawbox=x=0:y=946:w=1920:h=134:color=0x13261a:t=fill,ass={intro_ass.as_posix()},format=yuv420p[v]')
intro=work/'intro.mp4'
if not args.reuse_intro or not intro.exists():run(cmd+['-filter_complex',';'.join(filters),'-map','[v]','-an','-t',str(intro_duration),'-r','30','-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-y',str(intro)])
elapsed=intro_duration
for idx,s in enumerate(scenes):
 duration=float(s['target']);local=[]
 for j,en in enumerate(s['cues']):
  start=j*duration/len(s['cues']);end=(j+1)*duration/len(s['cues'])
  local.append((start,end,en))
 subtitle=work/f'{s["id"]}.ass';lines=[header]
 lines.append(f'Dialogue: 1,0:00:00.00,{ass_time(duration)},Label,,0,0,0,,{s["label"]}\n')
 if s.get('stock'):
  lines.append(f'Dialogue: 1,0:00:00.00,{ass_time(duration)},Notice,,0,0,0,,Illustrative stock footage / fictional scenario\\N{s["stock"]}\n')
 else:
  lines.append(f'Dialogue: 1,0:00:00.00,{ass_time(duration)},Notice,,0,0,0,,{{\\an9\\pos(1758,15)\\fs18}}Edited live app recording / fictional demo data\n')
 if s.get('auth'):lines.append(f'Dialogue: 2,0:00:00.00,{ass_time(duration)},Notice,,0,0,0,,{{\\an7\\pos(18,88)\\fs20\\bord0}}LOCAL TEST\\NOTP ONLY\\NNO EMAIL\n')
 if s.get('outro'):lines.append(f'Dialogue: 2,0:00:00.50,{ass_time(duration-.3)},Title,,0,0,0,,{{\\fad(450,450)\\pos(960,440)}}Village Jobs\\N{{\\fs32}}A first conversation. A local opportunity.\n')
 for a,b,en in local:
  end=b;lines.append(f'Dialogue: 3,{ass_time(a)},{ass_time(end)},Caption,,0,0,0,,{ass(en)}\n');global_cues.append((elapsed+a,elapsed+end,en));
 subtitle.write_text(''.join(lines))
 # Cut native video sources, concatenate motion, and retime only for editorial pacing.
 cmd=[ff,'-hide_banner','-loglevel','error'];filters=[];raw_length=sum(part[2] for part in s['parts'])
 for i,(file,start,length) in enumerate(s['parts']):
  cmd+=['-ss',str(start),'-t',str(length),'-i',str(raw/file)]
  filters.append(f'[{i}:v]setpts=PTS-STARTPTS,fps=30,scale=1600:900,setsar=1[p{i}]')
 merged=''.join(f'[p{i}]' for i in range(len(s['parts'])))
 filters.append(f'{merged}concat=n={len(s["parts"])}:v=1:a=0,setpts={duration/raw_length:.9f}*PTS,fps=30,trim=duration={duration:.4f}[joined]')
 if s.get('stock'):filters.append('[joined]scale=1920:1080,crop=1920:1080,drawbox=x=0:y=0:w=iw:h=135:color=0x13261a@0.75:t=fill[canvas]')
 else:filters.append('[joined]pad=1920:1080:160:46:color=0x13261a[canvas]')
 if s.get('outro'):filters.append('[canvas]drawbox=x=0:y=0:w=iw:h=946:color=0x13261a@0.78:t=fill[dim]');canvas='dim'
 else:canvas='canvas'
 filters.append(f'[{canvas}]drawbox=x=0:y=946:w=1920:h=134:color=0x13261a:t=fill,ass={subtitle.as_posix()}[v]')
 clip=work/f'{s["id"]}.mp4'
 cmd+=['-filter_complex',';'.join(filters),'-map','[v]','-an','-t',str(duration),'-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart','-y',str(clip)]
 try:
  if not args.only or s['id'] in args.only.split(',') or not clip.exists():run(cmd)
 except subprocess.CalledProcessError as e:print(e.stderr.decode()[-8000:]);raise
 timeline.append({**s,'start':round(elapsed,3),'duration':round(duration,3),'cues':[{'start':round(a,3),'end':round(b,3),'en':en} for a,b,en in local]});elapsed+=duration;print(f'{s["id"]}: {duration:.2f}s / total {elapsed:.2f}s',flush=True)
assert elapsed<=180,f'Runtime too long: {elapsed:.2f}'
concat=work/'concat.txt';concat.write_text(f"file '{intro}'\n"+''.join(f"file '{work/(s['id']+'.mp4')}'\n" for s in scenes))
master=out/'village-jobs-photo-story-fast-en.mp4'
run([ff,'-hide_banner','-loglevel','error','-f','concat','-safe','0','-i',str(concat),'-c','copy','-metadata','title=Village Jobs — Korean photo story and live demo, English subtitles','-metadata','comment=Meta Muse Image fictional Korean photo story, animated stills, followed by native browser footage. No narration. Test authentication.','-movflags','+faststart','-y',str(master)])
(out/'village-jobs-photo-story-fast.en.srt').write_text(''.join(f'{i+1}\n{srt_time(a)} --> {srt_time(b)}\n{en}\n\n' for i,(a,b,en) in enumerate(global_cues)))
(out/'source'/'photo-story'/'edit-timeline.json').write_text(json.dumps(timeline,ensure_ascii=False,indent=2)+'\n')

print(json.dumps({'output':str(master),'duration':elapsed,'bytes':master.stat().st_size}))

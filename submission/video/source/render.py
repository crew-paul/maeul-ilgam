#!/usr/bin/env python3
"""Edit native browser MP4 recordings; never build UI footage from still images.
Usage: python3 render.py --raw-dir /tmp/village-film --ffmpeg /path/to/ffmpeg
Requires macOS say (Yuna) and FFmpeg with libass. Raw takes are retained separately.
"""
import argparse,json,subprocess,re,wave,shutil
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--only',help='Render only these comma-separated scene ids, then rebuild the master');p.add_argument('--raw-dir',type=Path,required=True);p.add_argument('--ffmpeg',default=shutil.which('ffmpeg'));p.add_argument('--output-dir',type=Path,default=Path(__file__).resolve().parents[1]);args=p.parse_args()
assert args.ffmpeg,'FFmpeg is required';ff=args.ffmpeg;raw=args.raw_dir;out=args.output_dir;work=raw/'edit';work.mkdir(exist_ok=True);out.mkdir(exist_ok=True)
scenes=json.loads(Path(__file__).with_name('storyboard.json').read_text())
def run(cmd):subprocess.run(cmd,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
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
global_cues=[];timeline=[];elapsed=0
for idx,s in enumerate(scenes):
 audio_parts=[];local=[];at=.22
 for j,(ko,en) in enumerate(s['cues']):
  base=work/f'{s["id"]}-{j}';txt=base.with_suffix('.txt');aiff=base.with_suffix('.aiff');wav=base.with_suffix('.wav');txt.write_text(ko)
  if not wav.exists():
   run(['say','-v','Yuna','-r','165','-f',str(txt),'-o',str(aiff)])
   run([ff,'-hide_banner','-loglevel','error','-i',str(aiff),'-ar','48000','-ac','1','-c:a','pcm_s16le','-y',str(wav)])
  with wave.open(str(wav)) as f:dur=f.getnframes()/f.getframerate()
  local.append((at,at+dur,en,ko));audio_parts.append((wav,at));at+=dur+.28
 duration=max(float(s['target']),at+.35)
 # Space captions with their actual speech. Unused time remains real recorded motion.
 spread=max(0,duration-(at+.35));shift=0
 if len(local)>1:spread=min(spread,2.0)
 for j in range(len(local)):
  a,b,en,ko=local[j];shift=spread*j/max(1,len(local)-1);local[j]=(a+shift,b+shift,en,ko);audio_parts[j]=(audio_parts[j][0],a+shift)
 subtitle=work/f'{s["id"]}.ass';lines=[header]
 lines.append(f'Dialogue: 1,0:00:00.00,{ass_time(duration)},Label,,0,0,0,,{s["label"]}\n')
 if s.get('stock'):
  lines.append(f'Dialogue: 1,0:00:00.00,{ass_time(duration)},Notice,,0,0,0,,Illustrative stock footage / fictional scenario\\N{s["stock"]}\n')
 else:
  lines.append(f'Dialogue: 1,0:00:00.00,{ass_time(duration)},Notice,,0,0,0,,{{\\an9\\pos(1758,15)\\fs18}}Edited live app recording / fictional demo data\n')
 if s.get('auth'):lines.append(f'Dialogue: 2,0:00:00.00,{ass_time(duration)},Notice,,0,0,0,,{{\\an7\\pos(18,88)\\fs20\\bord0}}LOCAL TEST\\NOTP ONLY\\NNO EMAIL\n')
 if s.get('outro'):lines.append(f'Dialogue: 2,0:00:00.50,{ass_time(duration-.3)},Title,,0,0,0,,{{\\fad(450,450)\\pos(960,440)}}Village Jobs\\N{{\\fs32}}A first conversation. A local opportunity.\n')
 for a,b,en,ko in local:
  end=min(duration,b+.12);lines.append(f'Dialogue: 3,{ass_time(a)},{ass_time(end)},Caption,,0,0,0,,{ass(en)}\n');global_cues.append((elapsed+a,elapsed+end,en));
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
 for wav,a in audio_parts:cmd+=['-i',str(wav)]
 offset=len(s['parts'])
 for j,(_,a) in enumerate(audio_parts):filters.append(f'[{offset+j}:a]adelay={round(a*1000)}:all=1,apad,atrim=duration={duration:.4f}[a{j}]')
 filters.append(''.join(f'[a{j}]' for j in range(len(audio_parts)))+f'amix=inputs={len(audio_parts)}:normalize=0,alimiter=limit=0.95[a]')
 clip=work/f'{s["id"]}.mp4'
 cmd+=['-filter_complex',';'.join(filters),'-map','[v]','-map','[a]','-t',str(duration),'-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-ar','48000','-movflags','+faststart','-y',str(clip)]
 try:
  if not args.only or s['id'] in args.only.split(',') or not clip.exists():run(cmd)
 except subprocess.CalledProcessError as e:print(e.stderr.decode()[-8000:]);raise
 timeline.append({**s,'start':round(elapsed,3),'duration':round(duration,3),'cues':[{'start':round(a,3),'end':round(b,3),'ko':ko,'en':en} for a,b,en,ko in local]});elapsed+=duration;print(f'{s["id"]}: {duration:.2f}s / total {elapsed:.2f}s',flush=True)
assert elapsed<=180,f'Runtime too long: {elapsed:.2f}'
concat=work/'concat.txt';concat.write_text(''.join(f"file '{work/(s['id']+'.mp4')}'\n" for s in scenes))
master=out/'village-jobs-demo-ko-en.mp4'
run([ff,'-hide_banner','-loglevel','error','-f','concat','-safe','0','-i',str(concat),'-c','copy','-metadata','title=Village Jobs — narrated in Korean, English subtitles','-metadata','comment=Actual native browser MP4 captures edited with licensed illustrative stock footage. Local test authentication.','-metadata:s:a:0','language=kor','-movflags','+faststart','-y',str(master)])
(out/'village-jobs-demo.en.srt').write_text(''.join(f'{i+1}\n{srt_time(a)} --> {srt_time(b)}\n{en}\n\n' for i,(a,b,en) in enumerate(global_cues)))
(out/'source'/'edit-timeline.json').write_text(json.dumps(timeline,ensure_ascii=False,indent=2)+'\n')
(out/'source'/'narration-ko.txt').write_text('\n\n'.join(' '.join(c[0] for c in s['cues']) for s in scenes)+'\n')
print(json.dumps({'output':str(master),'duration':elapsed,'bytes':master.stat().st_size}))

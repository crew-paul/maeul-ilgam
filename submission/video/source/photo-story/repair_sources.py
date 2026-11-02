#!/usr/bin/env python3
"""Remove explicitly reviewed capture glitches before frame-rate conversion; keep originals."""
import argparse,subprocess,json,hashlib
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--raw-dir',type=Path,required=True);p.add_argument('--cleaned-dir',type=Path,required=True);p.add_argument('--ffmpeg',required=True);a=p.parse_args()
manifest=json.loads(Path(__file__).with_name('source-frame-repairs.json').read_text());a.cleaned_dir.mkdir(parents=True,exist_ok=True)
for s in manifest['sources']:
 src=a.raw_dir/s['file'];dst=a.cleaned_dir/s['file'];marker=dst.with_suffix('.repair.json')
 assert hashlib.sha256(src.read_bytes()).hexdigest()==s['sha256'],f'Original recording differs: {src}'
 signature=hashlib.sha256(json.dumps(s,sort_keys=True).encode()).hexdigest()
 if dst.exists() and marker.exists() and json.loads(marker.read_text()).get('signature')==signature:
  print('Reuse repaired source:',s['file'],flush=True);continue
 terms='+'.join(f"eq(n,{f['index']})" for f in s['excludedFrames']) or '0'
 vf=f"select='not({terms})',tpad=stop_mode=clone:stop_duration=1,fps=fps=30:start_time=0:round=near,scale=1600:900:in_range=pc:out_range=tv,format=yuv420p,setsar=1,trim=duration={s['durationSeconds']}"
 r=subprocess.run([a.ffmpeg,'-v','error','-i',str(src),'-vf',vf,'-an','-c:v','libx264','-preset','fast','-crf','16','-pix_fmt','yuv420p','-color_range','tv','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-movflags','+faststart','-y',str(dst)],capture_output=True)
 if r.returncode:raise RuntimeError(r.stderr.decode()[-4000:])
 marker.write_text(json.dumps({'signature':signature,'excludedSourceFrames':[x['index'] for x in s['excludedFrames']],'sourceSha256':s['sha256']},indent=2)+'\n')
 print('Repaired',s['file'],'excluded',len(s['excludedFrames']),'capture glitches',flush=True)

#!/usr/bin/env python3
"""Regression check for the observed half-size native-browser capture defect."""
import argparse,subprocess,json
from pathlib import Path

def scan(ffmpeg,movie):
 r=subprocess.run([ffmpeg,'-v','error','-ss','32.4','-i',str(movie),'-vf','crop=1600:900:160:46,scale=320:180,format=gray','-an','-f','rawvideo','-'],capture_output=True,check=True)
 data=r.stdout;size=320*180;assert len(data)%size==0
 defects=[]
 for index in range(len(data)//size):
  frame=data[index*size:(index+1)*size]
  # The bad captures have a scrollbar at half width and a completely blank right half.
  dark=max(sum(frame[y*320+x]<150 for y in range(3,85))/82 for x in range(156,162))
  blank=sum(frame[y*320+x]>245 for y in range(5,175,5) for x in range(180,315,5))/(34*27)
  if dark>.8 and blank>.98:defects.append({'demoFrame':index,'timeSeconds':round(32.4+index/30,6)})
 return {'demoFramesScanned':len(data)//size,'defectFrames':defects}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--ffmpeg',required=True);p.add_argument('--before',type=Path,required=True);p.add_argument('--after',type=Path,required=True);a=p.parse_args()
 before=scan(a.ffmpeg,a.before);after=scan(a.ffmpeg,a.after)
 assert before['defectFrames'],'Regression baseline did not reproduce the reported capture defect'
 assert after['demoFramesScanned']==before['demoFramesScanned']==2400
 assert not after['defectFrames'],after
 manifest=json.loads(Path(__file__).with_name('source-frame-repairs.json').read_text())
 result={'before':before,'after':after,'reviewedSourceFramesExcluded':sum(len(s['excludedFrames']) for s in manifest['sources']),'method':'Detect the observed half-width scrollbar plus blank right-half capture geometry on every demo frame. This is a targeted regression check, not a universal visual-quality guarantee.','visualReview':'Pending inspection of repaired frame neighborhoods'}
 Path(__file__).with_name('capture-repair-check.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({'beforeDefectFrames':len(before['defectFrames']),'afterDefectFrames':len(after['defectFrames']),'demoFramesScanned':after['demoFramesScanned']}))

#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, hashlib, json, uuid
from datetime import datetime, timezone
from pathlib import Path

FIELDS = ['audio_id','time_utc','audio_file','sha256','transcript_file','speaker_count','language','quality_note','review_status','notes']

def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')

def digest(path: Path):
    if not path.exists() or not path.is_file(): return ''
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1048576), b''): h.update(chunk)
    return h.hexdigest()

def read(path: Path):
    if not path.exists(): return []
    with path.open(newline='', encoding='utf-8-sig') as f: return list(csv.DictReader(f))

def write(path: Path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=FIELDS, extrasaction='ignore'); w.writeheader(); w.writerows(rows)

def add(path: Path, args):
    rows=read(path)
    row={'audio_id':str(uuid.uuid4()),'time_utc':now(),'audio_file':args.audio_file,'sha256':digest(Path(args.audio_file)),'transcript_file':args.transcript_file,'speaker_count':args.speaker_count,'language':args.language,'quality_note':args.quality_note,'review_status':'pending','notes':args.notes}
    rows.append(row); write(path, rows); return row

def main():
    p=argparse.ArgumentParser(description='Track audio transcription inputs, transcript files, and review status.')
    p.add_argument('log'); p.add_argument('--audio-file', required=True); p.add_argument('--transcript-file', default=''); p.add_argument('--speaker-count', default='unknown'); p.add_argument('--language', default='unknown'); p.add_argument('--quality-note', default=''); p.add_argument('--notes', default=''); p.add_argument('--list', action='store_true')
    a=p.parse_args(); path=Path(a.log)
    if a.list: print(json.dumps(read(path), indent=2)); return 0
    print(json.dumps(add(path,a), indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())

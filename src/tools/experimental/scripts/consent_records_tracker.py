#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, json, uuid
from datetime import datetime, timezone
from pathlib import Path

FIELDS = ['record_id','time_utc','participant_id','scope','recording','withdrawal','privacy_note','review_status','access_rule','reviewer']

def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')

def read(path: Path):
    if not path.exists(): return []
    with path.open(newline='', encoding='utf-8-sig') as handle: return list(csv.DictReader(handle))

def write(path: Path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, extrasaction='ignore')
        writer.writeheader(); writer.writerows(rows)

def add(path: Path, args):
    rows = read(path)
    row = {'record_id': str(uuid.uuid4()), 'time_utc': now(), 'participant_id': args.participant_id, 'scope': args.scope, 'recording': args.recording, 'withdrawal': args.withdrawal, 'privacy_note': args.privacy_note, 'review_status': args.review_status, 'access_rule': args.access_rule, 'reviewer': args.reviewer}
    rows.append(row); write(path, rows); return row

def main():
    parser = argparse.ArgumentParser(description='Track consent and research review records.')
    parser.add_argument('tracker'); parser.add_argument('--participant-id'); parser.add_argument('--scope', default=''); parser.add_argument('--recording', default='no'); parser.add_argument('--withdrawal', default=''); parser.add_argument('--privacy-note', default=''); parser.add_argument('--review-status', default='pending'); parser.add_argument('--access-rule', default='restricted'); parser.add_argument('--reviewer', default=''); parser.add_argument('--list', action='store_true')
    args = parser.parse_args(); path = Path(args.tracker)
    if args.list: print(json.dumps(read(path), indent=2)); return 0
    if not args.participant_id: parser.error('--participant-id is required unless --list is used')
    print(json.dumps(add(path, args), indent=2)); return 0

if __name__ == '__main__':
    raise SystemExit(main())

#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json
from datetime import date
from pathlib import Path
FIELDS=['record_class','retention_years','trigger','disposal_action','authority','notes']
def init(p:Path):
    with p.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader()
    return {'created':str(p),'fields':FIELDS}
def review(schedule:Path, inventory:Path):
    with schedule.open(newline='',encoding='utf-8-sig') as f: rules={r['record_class']:r for r in csv.DictReader(f)}
    with inventory.open(newline='',encoding='utf-8-sig') as f: rows=list(csv.DictReader(f))
    results=[]
    today=date.today()
    for r in rows:
        rule=rules.get(r.get('record_class',''),{})
        try: years=int(rule.get('retention_years','0') or 0); year=int((r.get('date') or r.get('created') or '9999')[:4]); due=(today.year-year)>=years
        except Exception: due=False
        results.append({'record':r.get('title') or r.get('record_id'),'record_class':r.get('record_class'),'rule_found':bool(rule),'due_for_review':due,'action':rule.get('disposal_action','review')})
    return {'records':len(rows),'results':results}
def main():
    p=argparse.ArgumentParser(description='Create retention schedules and review inventory against them.')
    p.add_argument('--init'); p.add_argument('--schedule'); p.add_argument('--inventory')
    a=p.parse_args()
    if a.init: print(json.dumps(init(Path(a.init)),indent=2)); return 0
    if not a.schedule or not a.inventory: p.error('use --init or --schedule and --inventory')
    print(json.dumps(review(Path(a.schedule),Path(a.inventory)),indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())

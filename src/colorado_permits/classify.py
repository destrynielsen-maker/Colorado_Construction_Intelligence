from __future__ import annotations
import re
from .models import Permit

EXCLUDE = re.compile(r"\b(re-?roof|roofing|mechanical|plumbing|electrical|solar|photovoltaic|sign|fence|pool|spa|demolition|demo\b|water heater|tenant improvement|tenant finish|addition|alteration|remodel|repair|deck|patio cover|revision)\b", re.I)
MULTI = re.compile(r"\b(multi[ -]?family|apartment|townhome|townhouse|duplex|triplex|fourplex|condo|minium|\d+\s*[- ]?unit|\d+\s*[- ]?plex)\b", re.I)
SINGLE = re.compile(r"\b(single[- ]family detached|single family detached|one family dwelling|new residence|new home|sfr|detached dwelling)\b", re.I)
COMMERCIAL = re.compile(r"\b(assembly building|business use building|factory use building|hotel building|institutional use building|mercantile use building|storage use building|warehouse|industrial building|school|hospital|office building|retail building|non-residential|nonresidential)\b", re.I)

def infer_units(text: str) -> int | None:
    values=[]
    for pattern in (r"\b(\d+)\s*[- ]?unit\b", r"\b(\d+)\s*[- ]?plex\b"):
        values += [int(x) for x in re.findall(pattern, text, flags=re.I)]
    return max(values) if values else None

def classify_permit(p: Permit) -> Permit:
    desc = (p.raw or {}).get("description", "") if isinstance(p.raw, dict) else ""
    text = " ".join([p.permit_type or "", p.building_use or "", p.project_name or "", desc])
    if p.units is None:
        p.units = infer_units(text)
    excluded = bool(EXCLUDE.search(text))
    if MULTI.search(text) and not excluded:
        p.classification="MULTIFAMILY"; p.qualifies=True; p.new_construction_confidence="HIGH"
    elif SINGLE.search(text) and not excluded:
        p.classification="SINGLE_FAMILY"; p.qualifies=True; p.new_construction_confidence="HIGH"
    elif COMMERCIAL.search(text) and not excluded:
        p.classification="COMMERCIAL"; p.qualifies=True; p.new_construction_confidence="HIGH"
    else:
        p.classification="OTHER"; p.qualifies=False; p.new_construction_confidence="LOW"
    if not p.qualifies:
        p.score=0; return p
    score={"MULTIFAMILY":40,"COMMERCIAL":30,"SINGLE_FAMILY":15}[p.classification]
    value=float(p.valuation or 0)
    if value>=10_000_000: score+=20
    elif value>=5_000_000: score+=15
    elif value>=1_000_000: score+=10
    elif value>=500_000: score+=5
    units=int(p.units or 0)
    if units>=100: score+=20
    elif units>=50: score+=15
    elif units>=20: score+=10
    elif units>=5: score+=5
    if p.contractor: score+=5
    if p.owner: score+=3
    p.score=min(score,100)
    return p

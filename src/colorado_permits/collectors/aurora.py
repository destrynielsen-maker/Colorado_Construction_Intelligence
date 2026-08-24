from __future__ import annotations
from datetime import datetime, timezone, timedelta
import requests
from .base import CollectionResult, new_session
from ..models import Permit

class AuroraCollector:
    name="Aurora"
    freshness_days=10
    layer_url="https://ags.auroragov.org/aurora/rest/services/OpenData/MapServer/44"
    query_url=layer_url+"/query"
    source_url=layer_url
    fields=["Permit_","IssueDate","FolderDesc","FolderGroupDesc","SubDesc","FolderDescription","valuation","Address"]

    def collect(self, session: requests.Session | None=None) -> CollectionResult:
        s=session or new_session(); permits=[]; offset=0; page_size=2000
        cutoff=(datetime.now(timezone.utc)-timedelta(days=550)).date().isoformat()
        while True:
            params={"where":"IssueDate IS NOT NULL","outFields":",".join(self.fields),"returnGeometry":"false","orderByFields":"IssueDate DESC","resultOffset":offset,"resultRecordCount":page_size,"f":"json"}
            response=s.get(self.query_url,params=params,timeout=60); response.raise_for_status(); payload=response.json()
            if "error" in payload: raise RuntimeError(f"Aurora ArcGIS error: {payload['error']}")
            features=payload.get("features",[])
            if not features: break
            for feature in features:
                a=feature.get("attributes",{}); issued=self._date(a.get("IssueDate")); number=str(a.get("Permit_") or "").strip()
                if not issued or not number: continue
                if issued<cutoff:
                    return CollectionResult(self.name,permits,self.layer_url,"Official City of Aurora Building Permits ArcGIS layer; rolling ~18 months")
                permit_type=str(a.get("SubDesc") or a.get("FolderDesc") or "").strip()
                description=str(a.get("FolderDescription") or "").strip()
                permits.append(Permit(state="CO",jurisdiction=self.name,permit_number=number,issued_date=issued,permit_type=permit_type,building_use=str(a.get("FolderGroupDesc") or "").strip() or None,project_name=description or None,address=str(a.get("Address") or "").strip(),valuation=self._money(a.get("valuation")),source_name="Aurora Building Permits Open Data",source_url=self.layer_url,raw={**a,"description":description}))
            if len(features)<page_size: break
            offset+=len(features)
            if offset>100_000: raise RuntimeError("Aurora pagination safety limit exceeded")
        return CollectionResult(self.name,permits,self.layer_url,"Official City of Aurora Building Permits ArcGIS layer; rolling ~18 months")

    @staticmethod
    def _date(value):
        try: return datetime.fromtimestamp(int(value)/1000,tz=timezone.utc).date().isoformat()
        except (TypeError,ValueError,OSError): return None

    @staticmethod
    def _money(value):
        if value in (None,""): return None
        try: return float(str(value).replace("$","").replace(",","").strip())
        except ValueError: return None

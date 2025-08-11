
import os, math, psycopg2, spacy
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
API_KEY=os.getenv("WORKER_API_KEY",""); DATABASE_URL=os.getenv("DATABASE_URL")
nlp=spacy.load("en_core_web_sm"); app=FastAPI()
class EnrichReq(BaseModel): article_id:str
def db(): return psycopg2.connect(DATABASE_URL)
def themes(t:str):
  t=t.lower(); arr=[]
  if any(k in t for k in ["decree","tariff","sanction","subsid","regulat","licens"]): arr.append(("Policy Shift",0.85))
  if any(k in t for k in ["port","outage","congestion","shipment","supply","export ban","capacity"]): arr.append(("Supply Chain",0.75))
  if any(k in t for k in ["fx","currency","peg","capital control","remittance","depreciat"]): arr.append(("Geo/FX",0.7))
  if any(k in t for k in ["chip","semiconductor","subsea","latency","telecom","ai","cloud"]): arr.append(("Tech/Infra",0.7))
  if any(k in t for k in ["oil","gas","lithium","copper","nickel","harvest","crop","drought"]): arr.append(("Energy/Metals",0.7))
  if any(k in t for k in ["agri","weather","monsoon","planting","yield"]): arr.append(("Climate/Agri",0.6))
  if not arr: arr.append(("General",0.4))
  return arr
def score(w,n,l,s): return min(100.0, round(60*w + 15*(1 if s else 0) + 10*math.tanh(n/5) + 5*math.tanh(l/1500) + 2.5, 2))
@app.post("/enrich")
def enrich(req: EnrichReq, x_api_key: str = Header(default="")):
  if API_KEY and x_api_key != API_KEY: raise HTTPException(status_code=401, detail="bad api key")
  try: aid=int(req.article_id)
  except: raise HTTPException(status_code=400, detail="bad article id")
  conn=db(); conn.autocommit=True; cur=conn.cursor()
  cur.execute('SELECT title,"rawText",summary FROM "Article" WHERE id=%s',(aid,)); row=cur.fetchone()
  if not row: raise HTTPException(status_code=404, detail="article not found")
  title,raw,summary=row; text=" ".join([t for t in [title or "",raw or "",summary or ""] if t]).strip() or (title or "")
  doc=nlp(text); ents=[(e.text.strip(), e.label_) for e in doc.ents if e.label_ in ["GPE","ORG","NORP","PRODUCT","PERSON"]]
  for name,label in ents[:25]:
    cur.execute('INSERT INTO "Entity"(name,type) VALUES (%s,%s) ON CONFLICT DO NOTHING',(name,label))
    cur.execute('SELECT id FROM "Entity" WHERE name=%s LIMIT 1',(name,)); eid=cur.fetchone()[0]
    cur.execute('INSERT INTO "ArticleEntity"("articleId","entityId",confidence,sentiment) VALUES (%s,%s,%s,%s) ON CONFLICT DO NOTHING',(aid,eid,0.8,0.0))
  tlist=themes(text); specific=any(len(n)>1 and any(c.isupper() for c in n) for n,_ in ents)
  for theme,tw in tlist[:2]:
    sc=score(tw,len(ents),len(text),specific)
    cur.execute('INSERT INTO "Signal"("articleId",theme,score,rationale,region) VALUES (%s,%s,%s,%s,%s)',
                (aid,theme,sc,f"{theme} indicators detected; {len(ents)} entities; specific names present: {specific}.",None))
  cur.close(); conn.close(); return {"ok": True, "signals_created": min(2,len(tlist))}

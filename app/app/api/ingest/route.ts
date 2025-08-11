
import { NextRequest } from "next/server"; import { spawn } from "child_process"; import path from "path";
export async function POST(_req: NextRequest){ try{ const script=path.join(process.cwd(),"..","scripts","ingest_rss.ts"); const child=spawn("npx",["tsx",script],{env:process.env}); child.unref(); return Response.json({ok:true}); }catch(e){ return Response.json({ok:false,error:String(e)},{status:500}); } }

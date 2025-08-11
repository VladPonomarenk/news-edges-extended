
import { prisma } from "@/lib/prisma";
export async function GET(){
  const rows=await prisma.signal.findMany({orderBy:[{score:"desc"},{createdAt:"desc"}],include:{article:{include:{entities:{include:{entity:true}},source:true}}},take:200});
  const data=rows.map(r=>({id:String(r.id),score:r.score,theme:r.theme,title:r.article.title,publishedAt:r.article.publishedAt.toISOString(),region:r.region,entities:r.article.entities.map(ae=>ae.entity.name),rationale:r.rationale,sourceCount:1,link:r.article.url}));
  return Response.json({data});
}

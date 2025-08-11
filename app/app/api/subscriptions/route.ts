
import { prisma } from "@/lib/prisma"; import { NextRequest } from "next/server";
export async function GET(){ const subs=await prisma.subscription.findMany({include:{watchlist:true}}); return Response.json({data:subs}); }
export async function POST(req: NextRequest){ const {email,minScore=70,watchlistId=null}=await req.json(); const s=await prisma.subscription.create({data:{email,minScore,watchlistId}}); return Response.json({data:s}); }


import { prisma } from "@/lib/prisma"; import { NextRequest } from "next/server";
export async function GET(req: NextRequest){ const userId=req.nextUrl.searchParams.get("userId")||"demo"; const lists=await prisma.watchlist.findMany({where:{userId},include:{entities:{include:{entity:true}}}}); return Response.json({data:lists}); }
export async function POST(req: NextRequest){ const body=await req.json(); const {userId="demo",name}=body; const wl=await prisma.watchlist.create({data:{userId,name}}); return Response.json({data:wl}); }

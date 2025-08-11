
#!/usr/bin/env tsx
import { readFileSync } from "fs"; import { fileURLToPath } from "url"; import path from "path"; import { PrismaClient } from "@prisma/client";
const prisma=new PrismaClient(); const __dirname=path.dirname(fileURLToPath(import.meta.url));
async function main(){ const feeds=JSON.parse(readFileSync(path.join(__dirname,"../feeds/feeds.json"),"utf8")); for(const f of feeds.rss){ await prisma.source.upsert({ where:{url:f.url}, update:{name:f.name,type:f.type}, create:{name:f.name,url:f.url,type:f.type} }); } console.log("Seeded sources."); }
main().finally(async()=>prisma.$disconnect());

import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {PGlite} from '@electric-sql/pglite';
// Server process memory only. Restarting intentionally clears all application data.
export async function openDatabase(){
 const db=new PGlite();await db.waitReady;
 await db.exec(await fs.readFile(path.join(path.dirname(fileURLToPath(import.meta.url)),'migrations/001_core.sql'),'utf8'));
 return db;
}

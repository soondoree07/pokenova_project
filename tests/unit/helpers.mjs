import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

export const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..')
export const readText = (rel) => fs.readFileSync(path.join(ROOT, rel), 'utf8')
export const readJson = (rel) => JSON.parse(readText(rel))
export const exists = (rel) => fs.existsSync(path.join(ROOT, rel))

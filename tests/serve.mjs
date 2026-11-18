// 개발 · 검증용 정적 서버 (의존성 없음). 쓰는 법: node tests/serve.mjs <포트>
// 배포(Cloudflare · Vercel cleanUrls)처럼 /pokedex → pokedex.html, / → index.html 로 보여 준다
import http from 'node:http'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const port = Number(process.argv[2] ?? 4100)
const TYPES = {
  '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.json': 'application/json',
  '.png': 'image/png', '.ico': 'image/x-icon', '.mp4': 'video/mp4', '.css': 'text/css',
  '.txt': 'text/plain; charset=utf-8', '.xml': 'application/xml', '.svg': 'image/svg+xml', '.webp': 'image/webp',
}

// 주소 → 보여 줄 파일 (없으면 null)
export function resolveFile(urlPath) {
  const clean = decodeURIComponent(urlPath.split('?')[0]).replace(/\/+$/, '') || '/index'
  const candidates = [clean, `${clean}.html`, `${clean}/index.html`]
  for (const candidate of candidates) {
    const file = path.join(root, candidate)
    if (!file.startsWith(root + path.sep)) return null
    if (fs.existsSync(file) && fs.statSync(file).isFile()) return file
  }
  return null
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  http.createServer((req, res) => {
    const file = resolveFile(req.url ?? '/')
    if (!file) { res.writeHead(404).end('not found'); return }
    res.writeHead(200, { 'content-type': TYPES[path.extname(file)] ?? 'application/octet-stream' })
    fs.createReadStream(file).pipe(res)
  }).listen(port, () => console.log(`http://localhost:${port}`))
}

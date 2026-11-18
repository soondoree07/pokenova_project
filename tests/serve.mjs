// 개발 · 검증용 정적 서버 (의존성 없음). 쓰는 법: node tests/serve.mjs <포트>
// 배포(Cloudflare · Vercel cleanUrls)처럼 /pokedex → pokedex.html, / → index.html 로 보여 준다
// 검증 중 실제 방문 통계가 쌓이지 않게 구글 통계 스크립트는 여기서만 뺀다(배포 파일은 그대로)
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

const GTAG = /<script async src="https:\/\/www\.googletagmanager\.com\/[^"]*"><\/script>/g
export const stripAnalytics = (html) => html.replace(GTAG, '<!-- 검증 서버: 구글 통계 뺌 -->')

// 영상은 브라우저가 Range 로 나눠 받는다. 206 으로 답하지 않으면 요청이 끊긴 것으로 보인다
function sendRange(req, res, file, type) {
  const size = fs.statSync(file).size
  const [, a, b] = /bytes=(\d*)-(\d*)/.exec(req.headers.range) ?? []
  const start = a ? Number(a) : 0
  const end = b ? Math.min(Number(b), size - 1) : size - 1
  res.writeHead(206, { 'content-type': type, 'accept-ranges': 'bytes', 'content-range': `bytes ${start}-${end}/${size}`, 'content-length': end - start + 1 })
  fs.createReadStream(file, { start, end }).pipe(res)
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  http.createServer((req, res) => {
    const file = resolveFile(req.url ?? '/')
    if (!file) { res.writeHead(404).end('not found'); return }
    const type = TYPES[path.extname(file)] ?? 'application/octet-stream'
    if (req.headers.range) { sendRange(req, res, file, type); return }
    if (file.endsWith('.html')) { res.writeHead(200, { 'content-type': type }).end(stripAnalytics(fs.readFileSync(file, 'utf8'))); return }
    res.writeHead(200, { 'content-type': type, 'accept-ranges': 'bytes' })
    fs.createReadStream(file).pipe(res)
  }).listen(port, () => console.log(`http://localhost:${port}`))
}

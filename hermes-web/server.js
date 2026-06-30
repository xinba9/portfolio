#!/usr/bin/env node
/**
 * Hermes Web Chat - Node.js Local Proxy Server v4
 * Fixes all Python SSL/cert issues by using Node.js native https.
 * Serves HTML + proxies /api/chat to NVIDIA API.
 */

const http = require('http');
const https = require('https');
const fs = require('fs');
const path = require('path');

const PORT = 8765;
const API_BASE = 'https://integrate.api.nvidia.com/v1';
const API_KEY = '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';

// Read HTML file at startup
const htmlPath = path.join(__dirname, 'index.html');
let htmlContent = '';
try {
  htmlContent = fs.readFileSync(htmlPath, 'utf8');
  console.log(`[OK] Loaded index.html (${htmlContent.length} bytes)`);
} catch (e) {
  console.error(`[ERROR] Cannot read index.html: ${e.message}`);
  process.exit(1);
}

/**
 * Proxy a chat request to NVIDIA API
 */
function proxyChat(req, res) {
  let body = '';

  req.on('data', chunk => { body += chunk; });
  req.on('end', () => {
    let payload;
    try {
      payload = JSON.parse(body);
    } catch (e) {
      res.writeHead(400, { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' });
      res.end(JSON.stringify({ error: { message: 'Invalid JSON body' } }));
      return;
    }

    const model = payload.model || 'z-ai/glm-5.1';
    const messages = payload.messages || [];
    const max_tokens = payload.max_tokens || 2048;
    const temperature = payload.temperature || 0.7;
    const stream = payload.stream !== false;

    console.log(`[API] model=${model} stream=${stream} msgs=${messages.length}`);

    const apiPayload = JSON.stringify({
      model,
      messages,
      max_tokens,
      temperature,
      stream
    });

    const options = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(apiPayload),
        'Authorization': `Bearer ${API_KEY}`,
        'Accept': stream ? 'text/event-stream' : 'application/json'
      },
      // Disable SSL verification (self-signed OK for proxy)
      rejectUnauthorized: false
    };

    const proxyReq = https.request(`${API_BASE}/chat/completions`, options, (proxyRes) => {
      console.log(`[API] NVIDIA responded: ${proxyRes.statusCode}`);

      // Forward status and headers to browser
      res.writeHead(proxyRes.statusCode, {
        ...proxyRes.headers,
        'Access-Control-Allow-Origin': '*',
        'Cache-Control': 'no-cache'
      });

      // Stream response to browser
      proxyRes.on('data', chunk => {
        try { res.write(chunk); } catch (e) { /* client disconnected */ }
      });
      proxyRes.on('end', () => {
        try { res.end(); } catch (e) {}
        console.log(`[API] Done`);
      });
    });

    proxyReq.on('error', (e) => {
      console.error(`[API] Proxy request error: ${e.message}`);
      if (!res.headersSent) {
        res.writeHead(502, { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' });
        res.end(JSON.stringify({ error: { message: `API connection failed: ${e.message}` } }));
      } else {
        try { res.end(); } catch (e2) {}
      }
    });

    proxyReq.write(apiPayload);
    proxyReq.end();
  });

  req.on('error', (e) => {
    console.error(`[API] Request error: ${e.message}`);
  });
}

/**
 * Main request handler
 */
const server = http.createServer((req, res) => {
  const urlPath = req.url.split('?')[0];

  // CORS preflight
  if (req.method === 'OPTIONS') {
    res.writeHead(204, {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type'
    });
    res.end();
    return;
  }

  // API proxy
  if (req.method === 'POST' && urlPath === '/api/chat') {
    proxyChat(req, res);
    return;
  }

  // Serve HTML (with anti-cache headers)
  if (req.method === 'GET' && (urlPath === '/' || urlPath === '/index.html')) {
    res.writeHead(200, {
      'Content-Type': 'text/html; charset=utf-8',
      'Cache-Control': 'no-store, no-cache, must-revalidate, proxy-revalidate',
      'Pragma': 'no-cache',
      'Expires': '0'
    });
    res.end(htmlContent);
    return;
  }

  // 404
  res.writeHead(404, { 'Content-Type': 'text/plain' });
  res.end('Not Found');
});

server.listen(PORT, '127.0.0.1', () => {
  console.log('==================================================');
  console.log('  Hermes Web Chat Server v4 (Node.js)');
  console.log(`  http://localhost:${PORT}`);
  console.log('==================================================');
  console.log('  Press Ctrl+C to stop\n');
});

server.on('error', (e) => {
  if (e.code === 'EADDRINUSE') {
    console.error(`[ERROR] Port ${PORT} is already in use. Please kill the existing process first.`);
  } else {
    console.error(`[ERROR] Server error: ${e.message}`);
  }
  process.exit(1);
});
